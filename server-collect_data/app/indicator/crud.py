from db import engine
from sqlalchemy import text
import pandas as pd

def update_with_indicators(df: pd.DataFrame, table: str):
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text(f"""
                UPDATE {table}
                SET rsi_14 = :rsi,
                    ema_20 = :ema,
                    macd = :macd,
                    macd_signal = :macd_signal,
                    boll_upper = :boll_upper,
                    boll_middle = :boll_middle,
                    boll_lower = :boll_lower,
                    processed = TRUE
                WHERE timestamp = :ts
            """), {
                "rsi": row.get("rsi_14"),
                "ema": row.get("ema_20"),
                "macd": row.get("macd"),
                "macd_signal": row.get("macd_signal"),
                "boll_upper": row.get("boll_upper"),
                "boll_middle": row.get("boll_middle"),
                "boll_lower": row.get("boll_lower"),
                "ts": row["timestamp"]
            })
