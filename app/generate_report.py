import os
import json
import hashlib
from datetime import datetime
from datetime import datetime

TODAY = datetime.utcnow().date().isoformat()
today_dt = datetime.utcnow()
intro_line = today_dt.strftime("Market Risk Monitor update for %B %d.")

from openai import OpenAI

from fetch_data import get_daily, get_vix, get_ovx, get_tnx
from signals import compute_signals
from generate_charts import generate_all_charts

os.makedirs("data", exist_ok=True)

DISCLAIMER = (
    "This is an automated market signal summary for informational purposes only. "
    "It is not financial advice."
)

# --------------------
# RSS Feed Function
# --------------------

import xml.etree.ElementTree as ET
from datetime import datetime as dt

RSS_FILE = "docs/feed.xml"

def update_rss(regime, summary, downturn_score, recovery_score, audio_url):

    os.makedirs("docs", exist_ok=True)

    now = dt.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    title = f"Market Regime: {regime}"
    link = "https://github.com/kam-reef/market-summary"

    description = f"""
    {DISCLAIMER}

    ---

    Regime: {regime}
    Downturn Score: {downturn_score}/3
    Recovery Score: {recovery_score}/3

    ---

    {summary}
    """

    # Create new item element
    item = ET.Element("item")

    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link

    desc = ET.SubElement(item, "description")
    desc.text = description

    ET.SubElement(item, "pubDate").text = now

    ET.SubElement(item, "guid").text = f"{TODAY}-{regime}"

    enclosure = ET.SubElement(item, "enclosure")
    enclosure.set("url", audio_url)
    enclosure.set("type", "audio/mpeg")

    # If file doesn't exist, create base structure
    if not os.path.exists(RSS_FILE):

        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")

        ET.SubElement(channel, "title").text = "Market Risk Monitor"
        ET.SubElement(channel, "link").text = link
        ET.SubElement(channel, "description").text = "Automated market regime signals"

        tree = ET.ElementTree(rss)
        tree.write(RSS_FILE)

    # Load existing XML
    tree = ET.parse(RSS_FILE)
    root = tree.getroot()
    channel = root.find("channel")

    # Insert new item at top
    channel.insert(0, item)

    # Keep only latest 1 items
    items = channel.findall("item")

    for old_item in items[1:]:
        channel.remove(old_item)

    # Save back
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

# --------------------
# AI Audio
# --------------------

from datetime import datetime

def generate_audio(summary):

    try:
        os.makedirs("audio", exist_ok=True)

        file_path = "audio/latest.mp3"

        # Intro + disclaimer
        today_dt = datetime.utcnow()
        intro_line = today_dt.strftime("Market Risk Monitor update for %B %d.")
        outtro_line = "Thank you for listening!"

        # Combine into final narration
        audio_text = f"{intro_line} ... {DISCLAIMER} ... {summary} ... {outtro_line}"

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
data["TNX"] = get_tnx()
data["OVX"] = get_ovx()

# --------------------
# Charts
# --------------------

generate_all_charts(data)

# --------------------
# Compute signals
# --------------------

signals, snapshot = compute_signals(data)

# --------------------
# Signal change detection
# --------------------

SIGNAL_HASH_FILE = "data/last_signal_hash.txt"
new_hash = hash_signals(signals)

old_hash = None
if os.path.exists(SIGNAL_HASH_FILE):
    with open(SIGNAL_HASH_FILE) as f:
        old_hash = f.read().strip()

if new_hash == old_hash:
    print("No signal change. Skipping run.")
    exit()


# --------------------
# Save signals + snapshot
# --------------------

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
# History tracking
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

history.append(history_entry)

with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=2)


# --------------------
# OpenAI summary
# --------------------

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = f"""
Market regime: {regime}

Signals:
{json.dumps(signals, indent=2)}

Snapshot:
{json.dumps(snapshot, indent=2)}

Write a short risk commentary followed by a bullet market summary.
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
# Update audio.mp3
# --------------------

audio_path = generate_audio(summary)
audio_url = "https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3"

# --------------------
# Update RSS feed.xml
# --------------------

update_rss(regime, summary, downturn_score, recovery_score, audio_url)

# --------------------
# Badge color
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

readme = f"""
# Market Risk Monitor

![Market Regime](https://img.shields.io/badge/Market%20Regime-{badge_label}-{badge_color})

**{regime}**  
**Score:** Downturn {downturn_score}/3 | Recovery {recovery_score}/3  
**Last Updated:** {TODAY}

---

⚠️ **Disclaimer**

This project is an experimental data pipeline and educational demonstration.
It is **not financial advice**. The signals and AI commentary are generated
automatically from public market data and may be incomplete, delayed, or
incorrect. Do not make investment decisions based solely on this repository.

---

## AI Risk Commentary

{summary}

[Audio](https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3)
[RSS](https://kam-reef.github.io/market-summary/feed.xml)

---

## Market Charts

### SPY Trend vs VIX
![Market Chart](charts/market_chart.png)

### ARKK Drawdown vs VIX
![ARKK VIX Chart](charts/arkk_vix_chart.png)

---

## Market Snapshot

- SPY: {snapshot["SPY"]["price"]} (200MA: {snapshot["SPY"]["ma200"]})
- QQQ: {snapshot["QQQ"]["price"]} (100MA: {snapshot["QQQ"]["ma100"]})
- ARKK 3M Change: {snapshot["ARKK"]["three_month_change_percent"]}%

- VIX: {snapshot["VIX"]["level"]}
- TNX (10Y Yield): {snapshot["TNX"]["yield"]}%
- OVX (Oil Volatility): {snapshot["OVX"]["level"]}

## Data

- Snapshot [data/market_snapshot.json](data/market_snapshot.json) 
- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)
"""

with open("README.md", "w") as f:
    f.write(readme)


# --------------------
# Save new hash
# --------------------

with open(SIGNAL_HASH_FILE, "w") as f:
    f.write(new_hash)