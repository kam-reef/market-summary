import os
import json

from openai import OpenAI

from fetch_data import get_daily
from signals import compute_signals


tickers = ["SPY","QQQ","ARKK","VIX"]

data = {}

for t in tickers:
    data[t] = get_daily(t)

signals = compute_signals(data)

os.makedirs("data", exist_ok=True)

with open("data/signals.json","w") as f:
    json.dump(signals,f,indent=2)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = f"""
These signals were generated from rule-based market indicators.

Signals:
{json.dumps(signals,indent=2)}

Write:
- Short risk commentary
- Bullet market summary

Mention that the raw signals are available in /data/signals.json
"""


resp = client.responses.create(
    model="gpt-5",
    input=prompt
)

summary = resp.output_text


readme = f"""
# Market Risk Monitor

## AI Risk Commentary

{summary}

## Raw Signals

[data/signals.json](data/signals.json)
"""

with open("README.md","w") as f:
    f.write(readme)