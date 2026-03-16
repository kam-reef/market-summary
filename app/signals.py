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

    spy["ma200"] = moving_average(spy["close"], 200)
    qqq["ma100"] = moving_average(qqq["close"], 100)

    signals["SPY_below_200MA"] = bool(spy["close"].iloc[-1] < spy["ma200"].iloc[-1])
    signals["SPY_above_200MA"] = bool(spy["close"].iloc[-1] > spy["ma200"].iloc[-1])

    signals["QQQ_above_100MA"] = bool(qqq["close"].iloc[-1] > qqq["ma100"].iloc[-1])

    signals["ARKK_3mo_drop"] = bool(percent_change(arkk["close"], 63) <= -15)

    signals["VIX_over_25"] = bool(vix["close"].iloc[-1] > 25)
    signals["VIX_under_20"] = bool(vix["close"].iloc[-1] < 20)

    return signals