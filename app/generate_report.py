print("STARTING generate_report.py")
import os
import json
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, UTC

from openai import OpenAI

from fetch_data import get_daily, get_vix, get_ovx, get_tnx, get_macro_data
from signals import compute_signals
from generate_charts import generate_all_charts


TODAY = datetime.now(UTC).date().isoformat()

DISCLAIMER = (
    "This is an automated market signal summary for informational purposes only. "
    "It is not financial advice."
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

os.makedirs("data", exist_ok=True)


def hash_signals(signals):
    return hashlib.md5(json.dumps(signals, sort_keys=True).encode()).hexdigest()


print("Fetching data...")
data = {}
data["SPY"] = get_daily("SPY")
data["QQQ"] = get_daily("QQQ")
data["ARKK"] = get_daily("ARKK")
data["VIX"] = get_vix()
data["OVX"] = get_ovx()
data["TNX"] = get_tnx()

macro_data = get_macro_data()

print("Data fetched")
signals, snapshot = compute_signals(data, macro_data)

print("Updating signal hash...")
SIGNAL_HASH_FILE = "data/last_signal_hash.txt"
new_hash = hash_signals(signals)

old_hash = None
if os.path.exists(SIGNAL_HASH_FILE):
    with open(SIGNAL_HASH_FILE) as f:
        old_hash = f.read().strip()

signal_changed = new_hash != old_hash

print("Updating charts...")
try:
    generate_all_charts(data, macro_data)
except TypeError:
    generate_all_charts(data)

with open("data/signals.json", "w") as f:
    json.dump(signals, f, indent=2)

with open("data/market_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

print("Updating market regime...")
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

print("Updating history...")
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

print("Generating AI summary...")
prompt = f"""
Market regime: {regime}

Snapshot:
{json.dumps(snapshot, indent=2)}

Write a short risk commentary followed by a bullet-point market summary.

Requirements:
- Include mortgage rate and condition explicitly in the bullets
- Include income spread (SP dividend yield vs 10Y) explicitly in the bullets
- Include VIX, SPY trend, and yield context
- If conditions are unchanged, say they are stable
- Be concise and consistent in tone
- Mention raw data is available in /data
"""

response = client.responses.create(
    model="gpt-5-mini",
    reasoning={"effort": "minimal"},
    max_output_tokens=500,
    input=prompt
)

summary = getattr(response, "output_text", None)
if not summary:
    summary = "Market update unavailable."


def generate_audio(summary):
    try:
        print("Starting audio generation...")
        os.makedirs("audio", exist_ok=True)

        for f in os.listdir("audio"):
            if f.endswith(".mp3"):
                os.remove(os.path.join("audio", f))

        file_path = "audio/latest.mp3"

        intro = datetime.now(UTC).strftime(
            "Market Risk Monitor update for %B %d."
        )

        audio_text = f"{intro} ... {DISCLAIMER} ... {summary}"

        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=audio_text[:2000]
        )

        audio_bytes = speech.content if hasattr(speech, "content") else speech

        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        print("✅ Audio file written:", file_path)
        return file_path

    except Exception:
        import traceback
        print("🚨 Audio generation failed:")
        traceback.print_exc()
        return None


print("Generating audio...")
audio_path = generate_audio(summary)
print("Audio path:", audio_path)

print("Updating RSS...")
RSS_FILE = "docs/feed.xml"


def update_rss(regime, summary, audio_file):
    os.makedirs("docs", exist_ok=True)

    now = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
    link = "https://github.com/kam-reef/market-summary"
    audio_url = "https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3"

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

print("Updating badge...")
if "Downturn" in regime:
    badge_label = "Downturn"
    badge_color = "red"
elif "Recovery" in regime:
    badge_label = "Recovery"
    badge_color = "green"
else:
    badge_label = "Mixed"
    badge_color = "yellow"

# Safe display values
mortgage = snapshot.get("mortgage", {})
mortgage_rate = mortgage.get("rate")
mortgage_condition = mortgage.get("condition", "Unknown")
mortgage_rate_text = f"{mortgage_rate}%" if mortgage_rate is not None else "Data unavailable"

inc = snapshot.get("income_spread", {})
sp_div = inc.get("sp_div_yield")
ten_y = inc.get("ten_year_yield")
spread = inc.get("spread")
inc_regime = inc.get("regime", "Unknown")

sp_div_txt = f"{sp_div}%" if sp_div is not None else "Data unavailable"
ten_y_txt = f"{ten_y}%" if ten_y is not None else "Data unavailable"
spread_txt = f"{spread}%" if spread is not None else "Data unavailable"

print("Updating readme...")
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

### SPY Trailing Dividend Yield (proxy)
![Income Spread](charts/income_spread.png)

---

## Market Snapshot

- SPY: {snapshot["SPY"]["price"]} (200MA: {snapshot["SPY"]["ma200"]})
- QQQ: {snapshot["QQQ"]["price"]} (100MA: {snapshot["QQQ"]["ma100"]})
- ARKK 3M Change: {snapshot["ARKK"]["three_month_change_percent"]}%

- VIX: {snapshot["VIX"]["level"]}
- TNX (10Y Yield): {snapshot["TNX"]["yield"]}%
- OVX (Oil Volatility): {snapshot["OVX"]["level"]}

- Mortgage Rate: {mortgage_rate_text}
- Mortgage Condition: {mortgage_condition}

- S&P 500 Dividend Yield: {sp_div_txt}
- 10Y Yield (for spread): {ten_y_txt}
- Income Spread (Div - 10Y): {spread_txt}
- Income Regime: {inc_regime}

[View raw data](data/market_snapshot.json)

---

{audio_section}

---

## RSS Feed

https://kam-reef.github.io/market-summary/feed.xml

---

## Data

- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)
"""

with open("README.md", "w") as f:
    f.write(readme)

with open(SIGNAL_HASH_FILE, "w") as f:
    f.write(new_hash)