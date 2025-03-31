import pandas as pd
from psycopg2 import connect, sql
from shared.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
from fetcher.binance_client import fetch_from_binance, get_latest_timestamp, get_binance_start_time


def get_db_connection():
    return connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def table_exists(symbol, interval):
    table_name = f"{symbol}_{interval}"
    conn = get_db_connection()
    cursor = conn.cursor()

    query = sql.SQL("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = %s
    );
    """)
    cursor.execute(query, (table_name,))
    exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return exists

def create_dynamic_table(symbol, interval):
    table_name = f"{symbol}_{interval}"
    conn = get_db_connection()
    cursor = conn.cursor()

    create_table_query = sql.SQL("""
        CREATE TABLE {} (
            timestamp TIMESTAMPTZ PRIMARY KEY,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL
        );
    """).format(sql.Identifier(table_name))

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"📐 created table `{table_name}`")

def save_to_db(symbol, interval):
    table_name = f"{symbol}_{interval}"

    if not table_exists(symbol, interval):
        create_dynamic_table(symbol, interval)
        start_time = get_binance_start_time(symbol)
    else:
        start_time = get_latest_timestamp(symbol, interval)

    all_data = []
    while True:
        df = fetch_from_binance(symbol, interval, limit=1000, start_time=start_time)
        if df.empty:
            break
        all_data.append(df)
        start_time = df["timestamp"].iloc[-1]  # 다음 요청을 위한 기준 시간
        if len(df) < 1000:
            break

    if not all_data:
        print(f"{symbol} {interval} 데이터 없음")
        return

    final_df = pd.concat(all_data, ignore_index=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = sql.SQL("""
        INSERT INTO {} (timestamp, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (timestamp) DO NOTHING;
    """).format(sql.Identifier(table_name))

    for _, row in final_df.iterrows():
        cursor.execute(insert_query, (
            row["timestamp"], row["open"], row["high"], row["low"], row["close"], row["volume"]
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{symbol} {interval} 저장 완료 ({len(final_df)} rows)")
