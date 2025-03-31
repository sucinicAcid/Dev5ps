import os
import sys

# 내부 모듈 경로 등록
sys.path.append(os.path.join(os.path.dirname(__file__), 'server-collector', 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from config import SYMBOLS, INTERVALS
from fetcher.crud import get_db_connection
from psycopg2 import sql

def drop_all_ohlcv_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    for symbol in SYMBOLS:
        for interval in INTERVALS:
            table = f"{symbol}_{interval}"
            print(f"Dropping table `{table}`...")
            drop_query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table))
            try:
                cursor.execute(drop_query)
            except Exception as e:
                print(f"Failed to drop `{table}`: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("All OHLCV tables dropped.")

if __name__ == "__main__":
    drop_all_ohlcv_tables()

# docker-compose up --build db
# python delete_all_data.py