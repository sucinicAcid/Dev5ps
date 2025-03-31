import requests
import pandas as pd
from datetime import datetime, timezone

def get_binance_start_time(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1d&limit=1&startTime=0"
    response = requests.get(url).json()
    if isinstance(response, list) and len(response) > 0:
        first_trade_time = response[0][0]
        return datetime.fromtimestamp(first_trade_time / 1000, tz=timezone.utc)
    raise ValueError(f"Binance에서 {symbol}USDT 심볼의 첫 거래 시간을 가져올 수 없습니다.")

def get_latest_timestamp(symbol, interval):
    from fetcher.crud import get_db_connection
    from psycopg2 import sql
    table_name = f"{symbol}_{interval}"
    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL("SELECT MAX(timestamp) FROM {};").format(sql.Identifier(table_name))
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result is None:
        return get_binance_start_time(symbol)
    return result

def fetch_from_binance(symbol, interval, limit=1000, start_time=None):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval={interval}&limit={limit}"
    if start_time:
        url += f"&startTime={int(start_time.timestamp() * 1000)}"
    response = requests.get(url).json()
    data = [
        {
            "timestamp": datetime.fromtimestamp(e[0] / 1000, tz=timezone.utc),
            "open": float(e[1]),
            "high": float(e[2]),
            "low": float(e[3]),
            "close": float(e[4]),
            "volume": float(e[5])
        }
        for e in response
    ]
    return pd.DataFrame(data)