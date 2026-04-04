import os
import requests
import pandas as pd

API_KEY = os.getenv("MASSIVE_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

BASE = "https://api.massive.com/v2/aggs/ticker"


def get_daily(ticker):
    url = f"{BASE}/{ticker}/range/1/day/2023-01-01/2026-12-31"

    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": API_KEY
    }

    r = requests.get(url, params=params, timeout=10)
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
    df.columns = [col.upper() for col in df.columns]

    if "DATE" not in df.columns:
        raise Exception(f"Unexpected OVX format: columns={df.columns}")

    if "CLOSE" in df.columns:
        value_col = "CLOSE"
    elif "OVX" in df.columns:
        value_col = "OVX"
    else:
        raise Exception(f"Unexpected OVX format: columns={df.columns}")

    df["date"] = pd.to_datetime(df["DATE"])
    df["close"] = df[value_col]

    return df[["date", "close"]]


def get_tnx():
    """
    10-Year Treasury Yield (FRED: DGS10) - historical
    """
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10"

    df = pd.read_csv(url)
    df.columns = ["date", "close"]

    df["date"] = pd.to_datetime(df["date"])
    df = df[df["close"] != "."]

    df["close"] = df["close"].astype(float)

    return df[["date", "close"]]


def fetch_fred_series(series_id):

    if not FRED_API_KEY:
        print("Missing FRED_API_KEY")
        return None

    try:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 10
        }

        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()

        data = r.json()

        for obs in data["observations"]:
            if obs["value"] != ".":
                return float(obs["value"])

        return None

    except Exception as e:
        print(f"FRED fetch failed for {series_id}: {e}")
        return None


def get_macro_data():
    return {
        "TNX": fetch_fred_series("DGS10"),
        "MORTGAGE30US": fetch_fred_series("MORTGAGE30US"),
    }