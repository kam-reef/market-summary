import os
import matplotlib.pyplot as plt


LOOKBACK_DAYS = 252


def trim(df):
    return df.tail(LOOKBACK_DAYS)


def save(fig, name):
    os.makedirs("charts", exist_ok=True)
    fig.savefig(f"charts/{name}.png", bbox_inches="tight")
    plt.close(fig)


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

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], color="black")

    ax.axhspan(25, df["close"].max(), color="red", alpha=0.1)
    ax.axhspan(0, 20, color="green", alpha=0.1)

    ax.set_title("VIX Level")

    save(fig, "vix")


# --------------------
# TNX
# --------------------

def chart_tnx(data):

    df = trim(data["TNX"].copy())

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], color="green")

    ax.axhline(4, linestyle="--", color="red")
    ax.axhline(3, linestyle="--", color="blue")

    ax.set_title("10-Year Treasury Yield")

    save(fig, "tnx")


# --------------------
# OVX
# --------------------

def chart_ovx(data):

    df = trim(data["OVX"].copy())

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(df["date"], df["close"], color="black")

    ax.axhline(40, linestyle="--", color="red")

    ax.set_title("Oil Volatility (OVX)")

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