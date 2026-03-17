import os
import matplotlib.pyplot as plt


LOOKBACK_DAYS = 252  # ~1 year


def trim(df):
    return df.tail(LOOKBACK_DAYS)


def generate_chart(data):

    spy = trim(data["SPY"].copy())
    vix = trim(data["VIX"].copy())

    spy["ma200"] = spy["close"].rolling(200).mean()

    fig, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(spy["date"], spy["close"], label="SPY", color="blue")
    ax1.plot(spy["date"], spy["ma200"], label="SPY 200MA", color="orange")
    ax1.set_ylabel("SPY Price")

    ax2 = ax1.twinx()
    ax2.plot(vix["date"], vix["close"], label="VIX", color="red", alpha=0.5)
    ax2.set_ylabel("VIX")

    plt.title("SPY Trend vs VIX (1Y)")

    fig.legend(loc="upper left")

    os.makedirs("charts", exist_ok=True)

    plt.savefig("charts/market_chart.png", bbox_inches="tight")
    plt.close()


def generate_arkk_vix_chart(data):

    arkk = trim(data["ARKK"].copy())
    vix = trim(data["VIX"].copy())

    arkk["pct_3mo"] = arkk["close"].pct_change(63) * 100

    fig, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(arkk["date"], arkk["pct_3mo"], label="ARKK 3M % Change", color="purple")
    ax1.axhline(-15, linestyle="--", color="black", label="-15% Threshold")
    ax1.set_ylabel("ARKK % Change")

    ax2 = ax1.twinx()
    ax2.plot(vix["date"], vix["close"], label="VIX", color="red", alpha=0.5)
    ax2.axhline(25, linestyle="--", color="red", label="VIX 25")
    ax2.set_ylabel("VIX")

    plt.title("ARKK Drawdown vs VIX Stress (1Y)")

    fig.legend(loc="upper left")

    os.makedirs("charts", exist_ok=True)

    plt.savefig("charts/arkk_vix_chart.png", bbox_inches="tight")
    plt.close()