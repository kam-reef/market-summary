import os
import requests
import pandas as pd
import yfinance as yf

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
            "sort_order": "asc",
            "observation_start": "2010-01-01",
            "limit": 100000
        }

        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        rows = []
        for obs in data.get("observations", []):
            v = obs.get("value")
            if v is None or v == ".":
                continue
            rows.append({
                "date": pd.to_datetime(obs["date"]),
                "close": float(v)
            })

        if not rows:
            return None

        df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
        return df

    except Exception as e:
        print(f"FRED fetch failed for {series_id}: {e}")
        return None


def fetch_sp500_dividend_yield_fallback():
    """
    Fallback source if FRED SPDIVY is unavailable.
    Uses Yahoo Finance trailing annual dividend yield for ^GSPC.
    Returns a DataFrame with one row: [date, close] in percent units.
    """
    try:
        t = yf.Ticker("^GSPC")
        info = t.info or {}
        y = info.get("dividendYield")  # often decimal, e.g. 0.0132

        if y is None:
            return None

        val = float(y)
        if val <= 1:
            val *= 100.0  # decimal -> percent

        return pd.DataFrame([{
            "date": pd.Timestamp.utcnow().normalize(),
            "close": val
        }])

    except Exception as e:
        print(f"SP500 dividend fallback failed: {e}")
        return None


def get_macro_data():
    spdivy = fetch_fred_series("SPDIVY")
    if spdivy is None or spdivy.empty:
        print("SPDIVY unavailable from FRED, using Yahoo fallback.")
        spdivy = fetch_sp500_dividend_yield_fallback()

    return {
        "MORTGAGE30US": fetch_fred_series("MORTGAGE30US"),
        "SPDIVY": spdivy,
        "DGS10": fetch_fred_series("DGS10"),
    }