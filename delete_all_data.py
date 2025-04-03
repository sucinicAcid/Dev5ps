import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

load_dotenv(dotenv_path=".env.local")


from shared.config import SYMBOLS, INTERVALS

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host = os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

def drop_all_ohlcv_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    for symbol in SYMBOLS:
        for interval in INTERVALS:
            table = f"{symbol}_{interval}".lower()
            print(f"🧹 Dropping table `{table}`...")
            drop_query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table))
            try:
                cursor.execute(drop_query)
            except Exception as e:
                print(f"`{table}` 삭제 실패: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("모든 OHLCV 테이블 삭제 완료.")

if __name__ == "__main__":
    drop_all_ohlcv_tables()



