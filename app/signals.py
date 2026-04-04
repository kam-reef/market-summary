def moving_average(series, window):
    return series.rolling(window).mean()


def percent_change(series, days):
    return (series.iloc[-1] / series.iloc[-days] - 1) * 100


def mortgage_signal(rate):
    if rate is None:
        return "Unknown"

    if rate < 5.75:
        return "Favorable"
    elif rate < 6.75:
        return "Neutral"
    else:
        return "Unfavorable"


def compute_signals(data, macro_data):

    spy = data["SPY"]
    qqq = data["QQQ"]
    arkk = data["ARKK"]
    vix = data["VIX"]
    tnx = data["TNX"]
    ovx = data["OVX"]

    signals = {}
    snapshot = {}

    # --------------------
    # Moving averages
    # --------------------

    spy["ma200"] = moving_average(spy["close"], 200)
    qqq["ma100"] = moving_average(qqq["close"], 100)

    # --------------------
    # Latest values
    # --------------------

    spy_price = float(spy["close"].iloc[-1])
    spy_ma200 = float(spy["ma200"].iloc[-1])

    qqq_price = float(qqq["close"].iloc[-1])
    qqq_ma100 = float(qqq["ma100"].iloc[-1])

    arkk_change = float(percent_change(arkk["close"], 63))

    vix_level = float(vix["close"].iloc[-1])
    tnx_level = float(tnx["close"].iloc[-1])
    ovx_level = float(ovx["close"].iloc[-1])

    mortgage_rate = macro_data.get("MORTGAGE30US")
    mortgage_condition = mortgage_signal(mortgage_rate)

    # --------------------
    # Core signals
    # --------------------

    signals["SPY_below_200MA"] = spy_price < spy_ma200
    signals["SPY_above_200MA"] = spy_price > spy_ma200

    signals["QQQ_above_100MA"] = qqq_price > qqq_ma100

    signals["ARKK_3mo_drop"] = arkk_change <= -15

    signals["VIX_over_25"] = vix_level > 25
    signals["VIX_under_20"] = vix_level < 20

    # --------------------
    # Macro signals
    # --------------------

    signals["TNX_above_4"] = tnx_level > 4.0
    signals["TNX_below_3"] = tnx_level < 3.0

    signals["OVX_low"] = ovx_level < 60
    signals["OVX_high"] = ovx_level > 90
    signals["OVX_mid"] = 60 <= ovx_level <= 90

    # --------------------
    # Snapshot (for README / AI)
    # --------------------

    snapshot["SPY"] = {
        "price": round(spy_price, 2),
        "ma200": round(spy_ma200, 2)
    }

    snapshot["QQQ"] = {
        "price": round(qqq_price, 2),
        "ma100": round(qqq_ma100, 2)
    }

    snapshot["ARKK"] = {
        "three_month_change_percent": round(arkk_change, 2)
    }

    snapshot["VIX"] = {
        "level": round(vix_level, 2)
    }

    snapshot["TNX"] = {
        "yield": round(tnx_level, 2)
    }

    snapshot["OVX"] = {
        "level": round(ovx_level, 2),
        "regime": "low" if ovx_level < 60 else "high" if ovx_level > 90 else "mid"
    }

    snapshot["mortgage"] = {
        "rate": round(mortgage_rate, 2) if mortgage_rate is not None else None,
        "condition": mortgage_condition
    }

    return signals, snapshot