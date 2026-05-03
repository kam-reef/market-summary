import os
import requests
import pandas as pd
import yfinance as yf

API_KEY = os.getenv("MASSIVE_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

BASE = "https://api.massive.com/v2/aggs/ticker"


def get_daily(ticker):
    url = f"{BASE}/{ticker}/range/1/day/2023-01-01/2026-12-31"
    params = {"adjusted": "true", "sort": "asc", "apiKey": API_KEY}

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
    df.columns = [c.upper() for c in df.columns]

    if "DATE" not in df.columns or "CLOSE" not in df.columns:
        raise Exception(f"Unexpected VIX format: columns={df.columns}")

    df["date"] = pd.to_datetime(df["DATE"])
    df["close"] = df["CLOSE"]
    return df[["date", "close"]]


def get_ovx():
    url = "https://cdn.cboe.com/api/global/us_indices/daily_prices/OVX_History.csv"
    df = pd.read_csv(url)
    df.columns = [c.upper() for c in df.columns]

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
            if v in (None, "."):
                continue
            rows.append({"date": pd.to_datetime(obs["date"]), "close": float(v)})

        if not rows:
            return None

        return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)

    except Exception as e:
        print(f"FRED fetch failed for {series_id}: {e}")
        return None


def get_spy_dividend_yield_proxy():
    """
    Robust equity income proxy:
    trailing 12M SPY dividends / latest SPY close * 100
    using yfinance.history() dividends column.
    Returns DataFrame [date, close] with one row.
    """
    try:
        t = yf.Ticker("SPY")
        hist = t.history(period="2y", auto_adjust=False)

        if hist is None or hist.empty:
            print("SPY history unavailable")
            return None

        if "Dividends" not in hist.columns:
            print("SPY history missing Dividends column")
            return None

        hist = hist.copy()
        hist.index = pd.to_datetime(hist.index).tz_localize(None)

        last_close = float(hist["Close"].dropna().iloc[-1])
        if last_close <= 0:
            return None

        cutoff = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=365)
        ttm_div = float(hist.loc[hist.index >= cutoff, "Dividends"].fillna(0).sum())

        if ttm_div <= 0:
            print("SPY TTM dividends are zero")
            return None

        yld = (ttm_div / last_close) * 100.0

        return pd.DataFrame([{
            "date": pd.Timestamp.utcnow().normalize(),
            "close": float(yld)
        }])

    except Exception as e:
        print(f"SPY dividend proxy fetch failed: {e}")
        return None


def get_macro_data():
    return {
        "MORTGAGE30US": fetch_fred_series("MORTGAGE30US"),
        "SPDIVY": get_spy_dividend_yield_proxy(),  # proxy, but stable
        "DGS10": fetch_fred_series("DGS10"),
    }