import pandas as pd
def calculate_bollinger(series: pd.Series, window: int = 20, num_std: float = 2.0):
    ma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper = ma + num_std * std
    lower = ma - num_std * std
    return ma, upper, lower