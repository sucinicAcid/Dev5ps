import pandas as pd
def calculate_macd(series: pd.Series):
    ema_12 = series.ewm(span=12).mean()
    ema_26 = series.ewm(span=26).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9).mean()
    return macd, signal