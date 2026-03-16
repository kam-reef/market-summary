def moving_average(series, window):
    return series.rolling(window).mean()


def percent_change(series, days):
    return (series.iloc[-1] / series.iloc[-days] - 1) * 100


def compute_signals(data):

    spy = data["SPY"]
    qqq = data["QQQ"]
    arkk = data["ARKK"]
    vix = data["VIX"]

    signals = {}
    snapshot = {}

    spy["ma200"] = moving_average(spy["close"], 200)
    qqq["ma100"] = moving_average(qqq["close"], 100)

    spy_price = float(spy["close"].iloc[-1])
    spy_ma200 = float(spy["ma200"].iloc[-1])

    qqq_price = float(qqq["close"].iloc[-1])
    qqq_ma100 = float(qqq["ma100"].iloc[-1])

    arkk_change = float(percent_change(arkk["close"], 63))

    vix_level = float(vix["close"].iloc[-1])

    signals["SPY_below_200MA"] = bool(spy_price < spy_ma200)
    signals["SPY_above_200MA"] = bool(spy_price > spy_ma200)

    signals["QQQ_above_100MA"] = bool(qqq_price > qqq_ma100)

    signals["ARKK_3mo_drop"] = bool(arkk_change <= -15)

    signals["VIX_over_25"] = bool(vix_level > 25)
    signals["VIX_under_20"] = bool(vix_level < 20)

    snapshot["SPY"] = {
        "price": round(spy_price,2),
        "ma200": round(spy_ma200,2)
    }

    snapshot["QQQ"] = {
        "price": round(qqq_price,2),
        "ma100": round(qqq_ma100,2)
    }

    snapshot["ARKK"] = {
        "three_month_change_percent": round(arkk_change,2)
    }

    snapshot["VIX"] = {
        "level": round(vix_level,2)
    }

    return signals, snapshot