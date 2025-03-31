import pandas as pd

def calculate_indicators(df):
    close = df["close"]
    df["rsi_14"] = 100 - (100 / (1 + (close.diff().clip(lower=0).rolling(14).mean() /
                                     -close.diff().clip(upper=0).rolling(14).mean())))
    df["ema_20"] = close.ewm(span=20, adjust=False).mean()
    df["macd"] = close.ewm(span=12, adjust=False).mean() - close.ewm(span=26, adjust=False).mean()
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    ma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    df["boll_upper"] = ma20 + 2 * std20
    df["boll_middle"] = ma20
    df["boll_lower"] = ma20 - 2 * std20
    return df
