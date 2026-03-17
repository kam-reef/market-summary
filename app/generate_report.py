import os
import json
import hashlib
from datetime import datetime

from openai import OpenAI

from fetch_data import get_daily, get_vix
from signals import compute_signals
from generate_charts import generate_chart, generate_arkk_vix_chart


TODAY = datetime.utcnow().date().isoformat()

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


# --------------------
# Charts
# --------------------

generate_chart(data)
generate_arkk_vix_chart(data)


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

⚠️ **Disclaimer**

This project is an experimental data pipeline and educational demonstration.
It is **not financial advice**. The signals and AI commentary are generated
automatically from public market data and may be incomplete, delayed, or
incorrect. Do not make investment decisions based solely on this repository.

Last Updated: {TODAY}

## Market Regime
{regime}

## AI Risk Commentary

{summary}

## Market Charts

### SPY Trend vs VIX
![Market Chart](charts/market_chart.png)

### ARKK Drawdown vs VIX
![ARKK VIX Chart](charts/arkk_vix_chart.png)

## Market Snapshot
[data/market_snapshot.json](data/market_snapshot.json)

## Raw Signals
[data/signals.json](data/signals.json)

## History
[data/history.json](data/history.json)
"""

with open("README.md", "w") as f:
    f.write(readme)


# --------------------
# Save new hash
# --------------------

with open(SIGNAL_HASH_FILE, "w") as f:
    f.write(new_hash)