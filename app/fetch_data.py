import os
import requests
import pandas as pd

API_KEY = os.getenv("MASSIVE_API_KEY")

BASE = "https://api.massive.com/v2/aggs/ticker"

def get_daily(ticker):

    url = f"{BASE}/{ticker}/range/1/day/2023-01-01/2026-12-31?adjusted=true&sort=asc&apiKey={API_KEY}"

    r = requests.get(url)
    r.raise_for_status()

    data = r.json()["results"]

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df["close"] = df["c"]

    return df[["date","close"]]