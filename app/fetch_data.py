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

    df.columns = [col.upper() for col in df.columns]

    if "DATE" not in df.columns or "CLOSE" not in df.columns:
        raise Exception(f"Unexpected VIX format: columns={df.columns}")

    df["date"] = pd.to_datetime(df["DATE"])
    df["close"] = df["CLOSE"]

    return df[["date", "close"]]

def get_ovx():

    url = "https://cdn.cboe.com/api/global/us_indices/daily_prices/OVX_History.csv"

    df = pd.read_csv(url)

    # Normalize column names
    df.columns = [col.upper() for col in df.columns]

    if "DATE" not in df.columns or "CLOSE" not in df.columns:
        raise Exception(f"Unexpected OVX format: columns={df.columns}")

    df["date"] = pd.to_datetime(df["DATE"])
    df["close"] = df["CLOSE"]

    return df[["date", "close"]]

def get_tnx():
    """
    10-Year Treasury Yield (FRED: DGS10)
    """

    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10"

    df = pd.read_csv(url)

    df.columns = ["date", "close"]

    df["date"] = pd.to_datetime(df["date"])

    # Remove missing values (FRED uses ".")
    df = df[df["close"] != "."]

    df["close"] = df["close"].astype(float)

    return df[["date", "close"]]