import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from app.fetcher.binance_client import fetch_from_binance, get_latest_timestamp, get_binance_start_time
from shared.db import engine
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def to_kst(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc).astimezone(KST)

def table_exists(symbol: str, interval: str) -> bool:
    table_name = f"{symbol}_{interval}"
    query = text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = :table_name
        );
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name})
        return result.scalar()


def create_dynamic_table(symbol: str, interval: str):
    table_name = f"{symbol}_{interval}"
    query = f"""
        CREATE TABLE "{table_name}" (
            timestamp TIMESTAMPTZ PRIMARY KEY,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL
        );
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        print(f"`{table_name}`이 생성되었습니다.")


def save_to_db(symbol: str, interval: str):
    table_name = f"{symbol}_{interval}"

    if not table_exists(symbol, interval):
        create_dynamic_table(symbol, interval)
        start_time = get_binance_start_time(symbol, interval)
    else:
        start_time = get_latest_timestamp(symbol, interval)

    all_data = []
    while True:
        df = fetch_from_binance(symbol, interval, limit=1000, start_time=start_time)
        if df.empty:
            break
        all_data.append(df)
        start_time = df["timestamp"].iloc[-1]
        if len(df) < 1000:
            break

    if not all_data:
        print(f"{symbol} {interval} 데이터 없음")
        return

    final_df = pd.concat(all_data, ignore_index=True)

    insert_query = f"""
        INSERT INTO "{table_name}" (timestamp, open, high, low, close, volume)
        VALUES (:timestamp, :open, :high, :low, :close, :volume)
        ON CONFLICT (timestamp) DO NOTHING;
    """

    with engine.begin() as conn:
        for _, row in final_df.iterrows():
            conn.execute(
                text(insert_query),
                {
                    "timestamp": to_kst(row["timestamp"]),
                    "open": row["open"],
                    "high": row["high"],
                    "low": row["low"],
                    "close": row["close"],
                    "volume": row["volume"],
                }
            )

    print(f"{symbol} {interval} 저장 완료 ({len(final_df)} rows)")