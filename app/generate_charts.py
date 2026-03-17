import os
import json
import matplotlib.pyplot as plt
import pandas as pd


LOOKBACK_DAYS = 252  # ~1 year


def trim(df):
    return df.tail(LOOKBACK_DAYS)


def load_history():
    path = "data/history.json"

    if not os.path.exists(path):
        return []

    with open(path) as f:
        return json.load(f)


def get_regime_periods():
    history = load_history()

    if not history:
        return []

    periods = []
    start_date = history[0]["date"]
    current_regime = history[0]["regime"]

    for entry in history[1:]:
        if entry["regime"] != current_regime:
            periods.append((start_date, entry["date"], current_regime))
            start_date = entry["date"]
            current_regime = entry["regime"]

    periods.append((start_date, history[-1]["date"], current_regime))

    return periods


def shade_regimes(ax, periods):

    for start, end, regime in periods:

        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        if "Downturn" in regime:
            color = "red"
        elif "Recovery" in regime:
            color = "green"
        else:
            color = "yellow"

        ax.axvspan(start, end, color=color, alpha=0.08)


def generate_chart(data):

    spy = trim(data["SPY"].copy())
    vix = trim(data["VIX"].copy())

    spy["ma200"] = spy["close"].rolling(200).mean()

    periods = get_regime_periods()

    fig, ax1 = plt.subplots(figsize=(10,5))

    # Background shading
    shade_regimes(ax1, periods)

    # SPY + MA
    ax1.plot(spy["date"], spy["close"], label="SPY", color="blue")
    ax1.plot(spy["date"], spy["ma200"], label="200MA", color="orange")

    below = spy["close"] < spy["ma200"]
    ax1.fill_between(spy["date"], spy["close"], spy["ma200"],
                     where=below, color="red", alpha=0.2,
                     label="Below 200MA")

    ax1.set_ylabel("SPY")

    # VIX
    ax2 = ax1.twinx()
    ax2.plot(vix["date"], vix["close"], label="VIX", color="black", alpha=0.6)

    ax2.axhspan(25, max(vix["close"]), color="red", alpha=0.1)
    ax2.axhspan(0, 20, color="green", alpha=0.1)

    ax2.set_ylabel("VIX")

    plt.title("SPY Trend vs VIX (Regime Shading)")

    fig.legend(loc="upper left")

    os.makedirs("charts", exist_ok=True)
    plt.savefig("charts/market_chart.png", bbox_inches="tight")
    plt.close()


def generate_arkk_vix_chart(data):

    arkk = trim(data["ARKK"].copy())
    vix = trim(data["VIX"].copy())

    arkk["pct_3mo"] = arkk["close"].pct_change(63) * 100

    periods = get_regime_periods()

    fig, ax1 = plt.subplots(figsize=(10,5))

    # Background shading
    shade_regimes(ax1, periods)

    ax1.plot(arkk["date"], arkk["pct_3mo"], label="ARKK 3M %", color="purple")

    drawdown = arkk["pct_3mo"] <= -15
    ax1.fill_between(arkk["date"], arkk["pct_3mo"], -15,
                     where=drawdown, color="red", alpha=0.3,
                     label=">15% Drop")

    ax1.axhline(-15, linestyle="--", color="black")

    ax1.set_ylabel("% Change")

    # VIX
    ax2 = ax1.twinx()
    ax2.plot(vix["date"], vix["close"], label="VIX", color="black", alpha=0.6)

    ax2.axhspan(25, max(vix["close"]), color="red", alpha=0.1)

    ax2.set_ylabel("VIX")

    plt.title("ARKK Drawdown vs VIX (Regime Shading)")

    fig.legend(loc="upper left")

    os.makedirs("charts", exist_ok=True)
    plt.savefig("charts/arkk_vix_chart.png", bbox_inches="tight")
    plt.close()