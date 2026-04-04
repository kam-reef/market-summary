import os
import json
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime

from openai import OpenAI

from fetch_data import get_daily, get_vix, get_ovx, get_tnx, get_macro_data
from signals import compute_signals
from generate_charts import generate_all_charts


TODAY = datetime.utcnow().date().isoformat()

DISCLAIMER = (
    "This is an automated market signal summary for informational purposes only. "
    "It is not financial advice."
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

os.makedirs("data", exist_ok=True)


# --------------------
# Helpers
# --------------------

def hash_signals(signals):
    return hashlib.md5(json.dumps(signals, sort_keys=True).encode()).hexdigest()


# --------------------
# Fetch data
# --------------------

data = {}

data["SPY"] = get_daily("SPY")
data["QQQ"] = get_daily("QQQ")
data["ARKK"] = get_daily("ARKK")
data["VIX"] = get_vix()
data["OVX"] = get_ovx()
data["TNX"] = get_tnx()

# ✅ NEW: macro data (FRED)
macro_data = get_macro_data()


# --------------------
# Compute signals
# --------------------

signals, snapshot = compute_signals(data, macro_data)


# --------------------
# Signal hash (still tracked)
# --------------------

SIGNAL_HASH_FILE = "data/last_signal_hash.txt"
new_hash = hash_signals(signals)

old_hash = None
if os.path.exists(SIGNAL_HASH_FILE):
    with open(SIGNAL_HASH_FILE) as f:
        old_hash = f.read().strip()

signal_changed = new_hash != old_hash


# --------------------
# Always update charts + data
# --------------------

generate_all_charts(data)

with open("data/signals.json", "w") as f:
    json.dump(signals, f, indent=2)

with open("data/market_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)


# --------------------
# Market regime
# --------------------

downturn_score = sum([
    signals["ARKK_3mo_drop"],
    signals["VIX_over_25"],
    signals["SPY_below_200MA"]
])

recovery_score = sum([
    signals["SPY_above_200MA"],
    signals["QQQ_above_100MA"],
    signals["VIX_under_20"]
])

if downturn_score >= 2:
    regime = "🔴 Downturn Risk"
elif recovery_score >= 2:
    regime = "🟢 Recovery"
else:
    regime = "🟡 Mixed Signals"


# --------------------
# History tracking (daily)
# --------------------

HISTORY_FILE = "data/history.json"

history_entry = {
    "date": TODAY,
    "regime": regime,
    "signals": signals
}

history = []

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE) as f:
        history = json.load(f)

if not history or history[-1]["date"] != TODAY:
    history.append(history_entry)

with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=2)


# --------------------
# Daily AI summary (ALWAYS)
# --------------------

prompt = f"""
Market regime: {regime}

Signals:
{json.dumps(signals, indent=2)}

Snapshot:
{json.dumps(snapshot, indent=2)}

Write a short risk commentary followed by a bullet market summary.

If signals have not changed, explicitly state that conditions are stable.
Mention mortgage conditions explicitly.
Mention the raw data files in /data.
"""

response = client.responses.create(
    model="gpt-5-mini",
    reasoning={"effort": "minimal"},
    max_output_tokens=500,
    input=prompt
)

summary = response.output_text


# --------------------
# Audio generation
# --------------------

audio_path = None

def generate_audio(summary):

    try:
        os.makedirs("audio", exist_ok=True)

        # remove old files
        for f in os.listdir("audio"):
            if f.endswith(".mp3"):
                os.remove(os.path.join("audio", f))

        file_path = "audio/latest.mp3"

        intro = datetime.utcnow().strftime(
            "Market Risk Monitor update for %B %d."
        )

        audio_text = f"{intro} ... {DISCLAIMER} ... {summary}"

        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=audio_text
        )

        with open(file_path, "wb") as f:
            f.write(speech.read())

        return file_path

    except Exception as e:
        print("Audio generation failed:", e)
        return None

# --------------------
# RSS update
# --------------------

RSS_FILE = "docs/feed.xml"

def update_rss(regime, summary, audio_file):

    os.makedirs("docs", exist_ok=True)

    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    link = "https://github.com/kam-reef/market-summary"

    audio_url = f"https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3"

    item = ET.Element("item")

    ET.SubElement(item, "title").text = f"Market Regime: {regime}"
    ET.SubElement(item, "link").text = link
    ET.SubElement(item, "pubDate").text = now
    ET.SubElement(item, "guid").text = now

    desc = ET.SubElement(item, "description")
    desc.text = f"{DISCLAIMER}\n\n{summary}"

    enclosure = ET.SubElement(item, "enclosure")
    enclosure.set("url", audio_url)
    enclosure.set("type", "audio/mpeg")

    if not os.path.exists(RSS_FILE):
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")

        ET.SubElement(channel, "title").text = "Market Risk Monitor"
        ET.SubElement(channel, "link").text = link
        ET.SubElement(channel, "description").text = "Daily market signal updates"

        tree = ET.ElementTree(rss)
        tree.write(RSS_FILE)

    tree = ET.parse(RSS_FILE)
    root = tree.getroot()
    channel = root.find("channel")

    channel.insert(0, item)

    items = channel.findall("item")
    for old_item in items[5:]:
        channel.remove(old_item)

    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)


if audio_path:
    update_rss(regime, summary, audio_path)


# --------------------
# Badge
# --------------------

if "Downturn" in regime:
    badge_label = "Downturn"
    badge_color = "red"
elif "Recovery" in regime:
    badge_label = "Recovery"
    badge_color = "green"
else:
    badge_label = "Mixed"
    badge_color = "yellow"


# --------------------
# README
# --------------------

audio_section = (
"## Latest Audio Update\n\n"
"[Listen to today's update](https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3)\n"
)

readme = f"""
# Market Risk Monitor

![Market Regime](https://img.shields.io/badge/Market%20Regime-{badge_label}-{badge_color})

**{regime}**  
**Score:** Downturn {downturn_score}/3 | Recovery {recovery_score}/3  
**Last Updated:** {TODAY}

---

⚠️ **Disclaimer**

{DISCLAIMER}

---

## AI Risk Commentary

{summary}

---

## Charts

### SPY Trend
![SPY](charts/spy.png)

### QQQ Trend
![QQQ](charts/qqq.png)

### ARKK Drawdown
![ARKK](charts/arkk.png)

### VIX
![VIX](charts/vix.png)

### 10Y Yield
![TNX](charts/tnx.png)

### Oil Volatility
![OVX](charts/ovx.png)

### Mortgage Conditions
![Mortgage](charts/mortgage.png)

---

## Market Snapshot

- SPY: {snapshot["SPY"]["price"]} (200MA: {snapshot["SPY"]["ma200"]})
- QQQ: {snapshot["QQQ"]["price"]} (100MA: {snapshot["QQQ"]["ma100"]})
- ARKK 3M Change: {snapshot["ARKK"]["three_month_change_percent"]}%

- VIX: {snapshot["VIX"]["level"]}
- TNX (10Y Yield): {snapshot["TNX"]["yield"]}%
- OVX (Oil Volatility): {snapshot["OVX"]["level"]}

- Mortgage Rate: {snapshot["mortgage"]["rate"]}%
- Mortgage Condition: {snapshot["mortgage"]["condition"]}

[View raw data](data/market_snapshot.json)

---

{audio_section}

---

## RSS Feed

Subscribe to daily updates:

https://kam-reef.github.io/market-summary/feed.xml

---

## Data

- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)

---

## Support

This is an automated, continuously running project built to answer practical questions about market conditions and retirement risk.

No content, no predictions—just data, rules, and outputs.

If you find it useful, you can support the project here:

- GitHub Sponsors (Pending)
- Buy Me a Coffee: https://buymeacoffee.com/yourname
"""

with open("README.md", "w") as f:
    f.write(readme)

with open(SIGNAL_HASH_FILE, "w") as f:
    f.write(new_hash)