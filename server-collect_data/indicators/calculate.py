from .rsi import calculate_rsi_and_sma_rsi
from .macd import calculate_macd
from .ema import calculate_ema
from .boll import calculate_bollinger
from .volume_ma import calculate_volume_ma


def calculate_indicators(df):
    df = df.copy()
    df["ema_7"] = calculate_ema(df["close"], 7)
    df["ema_25"] = calculate_ema(df["close"], 25)
    df["ema_99"] = calculate_ema(df["close"], 99)
    df["rsi"], df["rsi_signal"] = calculate_rsi_and_sma_rsi(df["close"])
    df["macd"], df["macd_signal"] = calculate_macd(df["close"])
    df["boll_ma"], df["boll_upper"], df["boll_lower"] = calculate_bollinger(
        df["close"], 20, 2.0
    )
    df["volume_ma_20"] = calculate_volume_ma(df["volume"], 20)
    return df
