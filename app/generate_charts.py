import os
import matplotlib.pyplot as plt
import pandas as pd

LOOKBACK_DAYS = 252  # ~1 trading year

def trim(df):
    return df.tail(LOOKBACK_DAYS)


def save(fig, name):
    os.makedirs("charts", exist_ok=True)
    fig.savefig(f"charts/{name}.png", bbox_inches="tight")
    plt.close(fig)


def add_regime_label(ax, label, color):
    ax.text(
        0.01, 0.95,
        f"Current: {label}",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor=color, alpha=0.2)
    )


def chart_spy(data):
    df = trim(data["SPY"].copy())
    df["ma200"] = df["close"].rolling(200).mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["close"], label="SPY", color="blue")
    ax.plot(df["date"], df["ma200"], label="200MA", color="orange")
    ax.fill_between(df["date"], df["close"], df["ma200"],
                    where=df["close"] < df["ma200"], color="red", alpha=0.2)
    ax.set_title("SPY vs 200-Day Moving Average")
    ax.legend()
    save(fig, "spy")


def chart_qqq(data):
    df = trim(data["QQQ"].copy())
    df["ma100"] = df["close"].rolling(100).mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["close"], label="QQQ", color="blue")
    ax.plot(df["date"], df["ma100"], label="100MA", color="orange")
    ax.fill_between(df["date"], df["close"], df["ma100"],
                    where=df["close"] < df["ma100"], color="red", alpha=0.2)
    ax.set_title("QQQ vs 100-Day Moving Average")
    ax.legend()
    save(fig, "qqq")


def chart_arkk(data):
    df = trim(data["ARKK"].copy())
    df["pct_3mo"] = df["close"].pct_change(63) * 100

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["pct_3mo"], color="purple")
    ax.axhline(-15, linestyle="--", color="black")
    ax.fill_between(df["date"], df["pct_3mo"], -15,
                    where=df["pct_3mo"] <= -15, color="red", alpha=0.3)
    ax.set_title("ARKK 3-Month % Change")
    save(fig, "arkk")


def chart_vix(data):
    df = trim(data["VIX"].copy())
    latest = float(df["close"].iloc[-1])

    if latest < 20:
        label, color = "Calm", "green"
    elif latest > 25:
        label, color = "Stress", "red"
    else:
        label, color = "Neutral", "yellow"

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["close"], color="black")
    ax.axhspan(0, 20, color="green", alpha=0.1)
    ax.axhspan(25, df["close"].max(), color="red", alpha=0.1)
    ax.axhline(20, linestyle="--", color="black")
    add_regime_label(ax, label, color)
    ax.set_title("VIX Regime")
    save(fig, "vix")


def chart_tnx(data):
    df = trim(data["TNX"].copy())
    latest = float(df["close"].iloc[-1])

    if latest < 3:
        label, color = "Supportive", "green"
    elif latest > 4:
        label, color = "Restrictive", "red"
    else:
        label, color = "Neutral", "yellow"

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["close"], color="blue")
    ax.axhspan(0, 3, color="green", alpha=0.1)
    ax.axhspan(4, df["close"].max(), color="red", alpha=0.1)
    ax.axhline(3.5, linestyle="--", color="black")
    add_regime_label(ax, label, color)
    ax.set_title("10-Year Treasury Yield Regime")
    save(fig, "tnx")


def chart_ovx(data):
    df = trim(data["OVX"].copy())
    latest = float(df["close"].iloc[-1])

    if latest < 60:
        label, color = "Low Vol", "green"
    elif latest > 90:
        label, color = "Extreme Stress", "red"
    else:
        label, color = "Elevated", "yellow"

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["close"], color="black")
    ax.axhspan(0, 60, color="green", alpha=0.1)
    ax.axhspan(90, df["close"].max(), color="red", alpha=0.1)
    ax.axhline(78, linestyle="--", color="black")
    add_regime_label(ax, label, color)
    ax.set_title("Oil Volatility (OVX) Regime")
    save(fig, "ovx")


def chart_mortgage(macro_data):
    df = macro_data.get("MORTGAGE30US")

    if df is None or df.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(0.5, 0.5, "Mortgage data unavailable", ha="center", va="center")
        ax.set_title("30-Year Fixed Mortgage Rate (FRED)")
        save(fig, "mortgage")
        return

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["date", "close"]).sort_values("date").tail(60)

    sma_window = 12
    df["sma"] = df["close"].rolling(sma_window).mean()

    latest = float(df["close"].iloc[-1])
    latest_sma = df["sma"].iloc[-1]

    if pd.notna(latest_sma) and latest > float(latest_sma):
        label, color = "Above SMA (upward pressure)", "red"
    elif pd.notna(latest_sma):
        label, color = "Below SMA (easing)", "green"
    else:
        label, color = "SMA warming up", "yellow"

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["close"], label="Mortgage Rate", color="purple", linewidth=2)
    ax.plot(df["date"], df["sma"], label=f"{sma_window}-Week SMA", color="orange", linewidth=2)

    mask = df["sma"].notna() & (df["close"] > df["sma"])
    ax.fill_between(df["date"], df["close"], df["sma"], where=mask, interpolate=True, color="red", alpha=0.25)

    add_regime_label(ax, label, color)
    ax.set_title("30-Year Fixed Mortgage Rate (FRED) vs SMA")
    ax.legend()
    save(fig, "mortgage")


def chart_income_spread(macro_data):
    """
    SP500 dividend yield vs 10Y Treasury spread:
    spread = SP500DY - DGS10
    """
    dy = macro_data.get("SP500DY")
    dgs10 = macro_data.get("DGS10") or macro_data.get("TNX")

    if dy is None or dgs10 is None or dy.empty or dgs10.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(0.5, 0.5, "Spread data unavailable (SP500DY / DGS10)", ha="center", va="center")
        ax.set_title("Income Spread: S&P 500 Dividend Yield - 10Y Treasury")
        save(fig, "income_spread")
        return

    dy = dy.copy()
    dgs10 = dgs10.copy()

    dy["date"] = pd.to_datetime(dy["date"])
    dgs10["date"] = pd.to_datetime(dgs10["date"])
    dy["close"] = pd.to_numeric(dy["close"], errors="coerce")
    dgs10["close"] = pd.to_numeric(dgs10["close"], errors="coerce")

    dy = dy.dropna(subset=["date", "close"])[["date", "close"]]
    dgs10 = dgs10.dropna(subset=["date", "close"])[["date", "close"]]

    merged = pd.merge(dy, dgs10, on="date", how="inner", suffixes=("_dy", "_10y"))
    merged = merged.sort_values("date").tail(252)

    if merged.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(0.5, 0.5, "No overlapping dates for SP500DY and DGS10", ha="center", va="center")
        ax.set_title("Income Spread: S&P 500 Dividend Yield - 10Y Treasury")
        save(fig, "income_spread")
        return

    merged["spread"] = merged["close_dy"] - merged["close_10y"]

    latest = float(merged["spread"].iloc[-1])
    if latest > 0:
        label, color = "Equity income > 10Y", "green"
    elif latest < 0:
        label, color = "10Y yield > equity income", "red"
    else:
        label, color = "Parity", "yellow"

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(merged["date"], merged["spread"], color="teal", linewidth=2, label="SP500DY - DGS10")
    ax.axhline(0, linestyle="--", color="black", linewidth=1)
    ax.fill_between(merged["date"], merged["spread"], 0, where=merged["spread"] > 0, color="green", alpha=0.15)
    ax.fill_between(merged["date"], merged["spread"], 0, where=merged["spread"] < 0, color="red", alpha=0.15)

    add_regime_label(ax, label, color)
    ax.set_title("Income Spread: S&P 500 Dividend Yield - 10Y Treasury")
    ax.legend()
    save(fig, "income_spread")


def generate_all_charts(data, macro_data=None):
    if macro_data is None:
        macro_data = {}

    chart_spy(data)
    chart_qqq(data)
    chart_arkk(data)
    chart_vix(data)
    chart_tnx(data)
    chart_ovx(data)
    chart_mortgage(macro_data)
    chart_income_spread(macro_data)