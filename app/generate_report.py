import os
import json
import hashlib
from datetime import datetime

from openai import OpenAI

from fetch_data import get_daily, get_vix, get_ovx, get_tnx
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
# Market regime (same logic as before)
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
# Event-based updates (ONLY on change)
# --------------------

summary = "No change in signals since last update."

if signal_changed:

    # ---- OpenAI summary ----
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


    # ---- History ----
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


    # ---- Save hash ----
    with open(SIGNAL_HASH_FILE, "w") as f:
        f.write(new_hash)

else:
    print("No signal change. Skipping AI / RSS / audio.")


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

---

## Market Snapshot

- SPY: {snapshot["SPY"]["price"]} (200MA: {snapshot["SPY"]["ma200"]})
- QQQ: {snapshot["QQQ"]["price"]} (100MA: {snapshot["QQQ"]["ma100"]})
- ARKK 3M Change: {snapshot["ARKK"]["three_month_change_percent"]}%

- VIX: {snapshot["VIX"]["level"]}
- TNX (10Y Yield): {snapshot["TNX"]["yield"]}%
- OVX (Oil Volatility): {snapshot["OVX"]["level"]}

[View raw data](data/market_snapshot.json)

---

## Data

- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)

---

## Support

This is an automated, continuously running project built to answer practical questions about market conditions and retirement risk.

No content, no predictions—just data, rules, and outputs.

If you find it useful, you can support the project here:

- GitHub Sponsors
- Buy Me a Coffee: https://buymeacoffee.com/yourname
"""

with open("README.md", "w") as f:
    f.write(readme)