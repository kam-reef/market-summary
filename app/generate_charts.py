import os
import matplotlib.pyplot as plt


def generate_chart(data):

    spy = data["SPY"]
    vix = data["VIX"]

    spy["ma200"] = spy["close"].rolling(200).mean()

    fig, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(spy["date"], spy["close"], label="SPY", color="blue")
    ax1.plot(spy["date"], spy["ma200"], label="SPY 200MA", color="orange")

    ax1.set_ylabel("SPY Price")

    ax2 = ax1.twinx()
    ax2.plot(vix["date"], vix["close"], label="VIX", color="red", alpha=0.5)
    ax2.set_ylabel("VIX")

    plt.title("Market Regime Indicators")

    fig.legend(loc="upper left")

    os.makedirs("charts", exist_ok=True)

    plt.savefig("charts/market_chart.png", bbox_inches="tight")
    plt.close()