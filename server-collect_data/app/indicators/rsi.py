import pandas as pd

def calculate_rsi(series: pd.Series, period: int = 14, signal_period: int = 9):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    rsi_signal = rsi.rolling(window=signal_period).mean()
    
    return rsi, rsi_signal
