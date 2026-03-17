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

    # SPY + MA
    ax1.plot(spy["date"], spy["close"], label="SPY", color="blue")
    ax1.plot(spy["date"], spy["ma200"], label="200MA", color="orange")

    # Highlight when SPY below 200MA
    below = spy["close"] < spy["ma200"]
    ax1.fill_between(spy["date"], spy["close"], spy["ma200"],
                     where=below, color="red", alpha=0.2,
                     label="Below 200MA")

    ax1.set_ylabel("SPY")

    # VIX
    ax2 = ax1.twinx()
    ax2.plot(vix["date"], vix["close"], label="VIX", color="black", alpha=0.6)

    # VIX stress zones
    ax2.axhspan(25, max(vix["close"]), color="red", alpha=0.1)
    ax2.axhspan(0, 20, color="green", alpha=0.1)

    ax2.set_ylabel("VIX")

    plt.title("SPY Trend vs VIX (Signal Context)")

    fig.legend(loc="upper left")

    os.makedirs("charts", exist_ok=True)
    plt.savefig("charts/market_chart.png", bbox_inches="tight")
    plt.close()


def generate_arkk_vix_chart(data):

    arkk = trim(data["ARKK"].copy())
    vix = trim(data["VIX"].copy())

    arkk["pct_3mo"] = arkk["close"].pct_change(63) * 100

    fig, ax1 = plt.subplots(figsize=(10,5))

    # ARKK drawdown
    ax1.plot(arkk["date"], arkk["pct_3mo"], label="ARKK 3M %", color="purple")

    # Highlight severe drawdown
    drawdown = arkk["pct_3mo"] <= -15
    ax1.fill_between(arkk["date"], arkk["pct_3mo"], -15,
                     where=drawdown, color="red", alpha=0.3,
                     label=">15% Drop")

    ax1.axhline(-15, linestyle="--", color="black")

    ax1.set_ylabel("% Change")

    # VIX overlay
    ax2 = ax1.twinx()
    ax2.plot(vix["date"], vix["close"], label="VIX", color="black", alpha=0.6)

    # VIX stress
    ax2.axhspan(25, max(vix["close"]), color="red", alpha=0.1)

    ax2.set_ylabel("VIX")

    plt.title("ARKK Drawdown vs VIX (Stress Signals)")

    fig.legend(loc="upper left")

    os.makedirs("charts", exist_ok=True)
    plt.savefig("charts/arkk_vix_chart.png", bbox_inches="tight")
    plt.close()