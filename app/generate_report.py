import os
import json
from datetime import datetime

from openai import OpenAI

from fetch_data import get_daily, get_vix
from signals import compute_signals


RUN_FILE = "data/last_run.txt"
TODAY = datetime.utcnow().date().isoformat()

os.makedirs("data", exist_ok=True)


# --------------------
# Fetch market data
# --------------------

data = {}

data["SPY"] = get_daily("SPY")
data["QQQ"] = get_daily("QQQ")
data["ARKK"] = get_daily("ARKK")
data["VIX"] = get_vix()


# --------------------
# Compute signals
# --------------------

signals = compute_signals(data)

with open("data/signals.json", "w") as f:
    json.dump(signals, f, indent=2)


# --------------------
# Market Regime
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
# Guardrail: only run OpenAI once per day
# --------------------

if os.path.exists(RUN_FILE):
    with open(RUN_FILE) as f:
        last_run = f.read().strip()

    if last_run == TODAY:
        print("Report already generated today. Skipping OpenAI call.")
        exit()


# --------------------
# OpenAI summary
# --------------------

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = f"""
These signals were generated from rule-based market indicators.

Signals:
{json.dumps(signals, indent=2)}

Market regime classification:
{regime}

Write:

1. Short risk commentary
2. Bullet market summary

Mention that the raw signals are available in /data/signals.json
"""

resp = client.responses.create(
    model="gpt-5-mini",
    max_output_tokens=300,
    input=prompt
)

summary = resp.output_text


# --------------------
# Generate README
# --------------------

readme = f"""
# Market Risk Monitor

Last Updated: {TODAY}

## Market Regime
{regime}

## AI Risk Commentary

{summary}

## Raw Signals

[data/signals.json](data/signals.json)
"""

with open("README.md", "w") as f:
    f.write(readme)


# --------------------
# Record run
# --------------------

with open(RUN_FILE, "w") as f:
    f.write(TODAY)