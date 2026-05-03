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


def get_spy_dividend_yield_from_massive():
    """
    Trailing 12M dividend yield proxy using SPY cash dividends / latest SPY close.
    Returns DataFrame with one row: [date, close] where close is yield in %.
    """
    if not API_KEY:
        print("Missing MASSIVE_API_KEY")
        return None

    try:
        spy = get_daily("SPY")
        if spy.empty:
            return None

        last_price = float(spy["close"].iloc[-1])
        if last_price <= 0:
            return None

        # Massive/Polygon-style dividends endpoint
        url = "https://api.massive.com/v3/reference/dividends"
        params = {
            "ticker": "SPY",
            "limit": 200,
            "sort": "ex_dividend_date",
            "order": "desc",
            "apiKey": API_KEY
        }

        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        rows = data.get("results", [])
        if not rows:
            print("No dividend rows returned for SPY")
            return None

        df = pd.DataFrame(rows)

        # Expected fields
        if "ex_dividend_date" not in df.columns or "cash_amount" not in df.columns:
            print(f"Unexpected dividend schema: {list(df.columns)}")
            return None

        df["ex_dividend_date"] = pd.to_datetime(df["ex_dividend_date"], errors="coerce")
        df["cash_amount"] = pd.to_numeric(df["cash_amount"], errors="coerce")
        df = df.dropna(subset=["ex_dividend_date", "cash_amount"])

        cutoff = pd.Timestamp.utcnow().normalize() - pd.Timedelta(days=365)
        ttm_div = float(df.loc[df["ex_dividend_date"] >= cutoff, "cash_amount"].sum())

        if ttm_div <= 0:
            print("TTM dividend sum is zero or missing")
            return None

        yield_pct = (ttm_div / last_price) * 100.0

        return pd.DataFrame([{
            "date": pd.Timestamp.utcnow().normalize(),
            "close": float(yield_pct)
        }])

    except Exception as e:
        print(f"Massive SPY dividend yield fetch failed: {e}")
        return None


def get_macro_data():
    return {
        "MORTGAGE30US": fetch_fred_series("MORTGAGE30US"),
        "SPDIVY": get_spy_dividend_yield_from_massive(),  # SPY proxy for equity dividend yield
        "DGS10": fetch_fred_series("DGS10"),
    }