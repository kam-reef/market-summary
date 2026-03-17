import os
import matplotlib.pyplot as plt


LOOKBACK_DAYS = 252


def trim(df):
    return df.tail(LOOKBACK_DAYS)


def save(fig, name):
    os.makedirs("charts", exist_ok=True)
    fig.savefig(f"charts/{name}.png", bbox_inches="tight")
    plt.close(fig)

# Chart stress labels

def add_regime_label(ax, label, color):

    ax.text(
        0.01, 0.95,
        f"Current: {label}",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor=color, alpha=0.2)
    )

# --------------------
# SPY (Trend)
# --------------------

def chart_spy(data):

    df = trim(data["SPY"].copy())
    df["ma200"] = df["close"].rolling(200).mean()

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], label="SPY", color="blue")
    ax.plot(df["date"], df["ma200"], label="200MA", color="orange")

    ax.fill_between(df["date"], df["close"], df["ma200"],
                    where=df["close"] < df["ma200"],
                    color="red", alpha=0.2)

    ax.set_title("SPY vs 200-Day Moving Average")

    ax.legend()

    save(fig, "spy")


# --------------------
# QQQ (Trend)
# --------------------

def chart_qqq(data):

    df = trim(data["QQQ"].copy())
    df["ma100"] = df["close"].rolling(100).mean()

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], label="QQQ", color="blue")
    ax.plot(df["date"], df["ma100"], label="100MA", color="orange")

    ax.fill_between(df["date"], df["close"], df["ma100"],
                    where=df["close"] < df["ma100"],
                    color="red", alpha=0.2)

    ax.set_title("QQQ vs 100-Day Moving Average")

    ax.legend()

    save(fig, "qqq")


# --------------------
# ARKK (Drawdown)
# --------------------

def chart_arkk(data):

    df = trim(data["ARKK"].copy())
    df["pct_3mo"] = df["close"].pct_change(63) * 100

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["pct_3mo"], color="purple")
    ax.axhline(-15, linestyle="--", color="black")

    ax.fill_between(df["date"], df["pct_3mo"], -15,
                    where=df["pct_3mo"] <= -15,
                    color="red", alpha=0.3)

    ax.set_title("ARKK 3-Month % Change")

    save(fig, "arkk")


# --------------------
# VIX
# --------------------

def chart_vix(data):

    df = trim(data["VIX"].copy())

    latest = float(df["close"].iloc[-1])

    if latest < 20:
        label, color = "Calm", "green"
    elif latest > 25:
        label, color = "Stress", "red"
    else:
        label, color = "Neutral", "yellow"

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], color="black")

    ax.axhspan(0, 20, color="green", alpha=0.1)
    ax.axhspan(25, df["close"].max(), color="red", alpha=0.1)

    ax.axhline(20, linestyle="--", color="black")

    add_regime_label(ax, label, color)

    ax.set_title("VIX Regime")

    save(fig, "vix")

# --------------------
# TNX
# --------------------

def chart_tnx(data):

    df = trim(data["TNX"].copy())

    latest = float(df["close"].iloc[-1])

    if latest < 3:
        label, color = "Supportive", "green"
    elif latest > 4:
        label, color = "Restrictive", "red"
    else:
        label, color = "Neutral", "yellow"

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], color="blue")

    ax.axhspan(0, 3, color="green", alpha=0.1)
    ax.axhspan(4, df["close"].max(), color="red", alpha=0.1)

    ax.axhline(3.5, linestyle="--", color="black")

    add_regime_label(ax, label, color)

    ax.set_title("10-Year Treasury Yield Regime")

    save(fig, "tnx")

# --------------------
# OVX
# --------------------

def chart_ovx(data):

    df = trim(data["OVX"].copy())

    latest = float(df["close"].iloc[-1])

    if latest < 60:
        label, color = "Low Vol", "green"
    elif latest > 90:
        label, color = "Extreme Stress", "red"
    else:
        label, color = "Elevated", "yellow"

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], color="black")

    ax.axhspan(0, 60, color="green", alpha=0.1)
    ax.axhspan(90, df["close"].max(), color="red", alpha=0.1)

    ax.axhline(78, linestyle="--", color="black")

    add_regime_label(ax, label, color)

    ax.set_title("Oil Volatility (OVX) Regime")

    save(fig, "ovx")


# --------------------
# Master function
# --------------------

def generate_all_charts(data):

    chart_spy(data)
    chart_qqq(data)
    chart_arkk(data)
    chart_vix(data)
    chart_tnx(data)
    chart_ovx(data)