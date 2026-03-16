import os
import requests
import pandas as pd

API_KEY = os.getenv("MASSIVE_API_KEY")

BASE = "https://api.massive.com/v2/aggs/ticker"


def get_daily(ticker):

    url = f"{BASE}/{ticker}/range/1/day/2023-01-01/2026-12-31"

    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": API_KEY
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    data = r.json()

    if "results" not in data or not data["results"]:
        raise Exception(f"Massive API error for {ticker}: {data}")

    df = pd.DataFrame(data["results"])

    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df["close"] = df["c"]

    return df[["date", "close"]]


def get_vix():

    url = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"

    df = pd.read_csv(url)

    df["date"] = pd.to_datetime(df["DATE"])
    df["close"] = df["CLOSE"]

    return df[["date", "close"]]