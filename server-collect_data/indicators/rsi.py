import pandas as pd


def rma(series: pd.Series, period: int) -> pd.Series:
    result = pd.Series(index=series.index, dtype="float64")
    series = series.copy()

    first_valid = series.first_valid_index()
    if first_valid is None:
        return result

    start = series.index.get_loc(first_valid) + period
    if start >= len(series):
        return result

    result.iloc[start] = series.iloc[start - period + 1 : start + 1].mean()
    for i in range(start + 1, len(series)):
        result.iloc[i] = (result.iloc[i - 1] * (period - 1) + series.iloc[i]) / period

    return result


def calculate_rsi_and_sma_rsi(close: pd.Series, rsi_period=14, smoothing_period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = rma(gain, rsi_period)
    avg_loss = rma(loss, rsi_period)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    smoothing_rsi = rsi.rolling(window=smoothing_period).mean()
    return rsi, smoothing_rsi
