import requests
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import text
from shared.db import engine

BINANCE_BASE_URL = "https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval={interval}&limit={limit}&startTime={start_time}"

def get_binance_start_time(symbol, interval, limit = 1, start_time = 0):
    url = BINANCE_BASE_URL.format(symbol=symbol, interval=interval.lower(), limit=limit, start_time=start_time)
    response = requests.get(url).json()
    if isinstance(response, list) and len(response) > 0:
        first_trade_time = response[0][0]
        return datetime.fromtimestamp(first_trade_time / 1000, tz=timezone.utc)
    raise ValueError(f"Binance에서 {symbol}_{interval}의 첫 거래 시간을 가져올 수 없습니다.")

def get_latest_timestamp(symbol, interval):
    table_name = f"{symbol}_{interval}"
    query = f"SELECT MAX(timestamp) FROM \"{table_name}\";"
    with engine.connect() as conn:
        result = conn.execute(text(query)).scalar()
    if result is None:
        return get_binance_start_time(symbol, interval)
    return result

def fetch_from_binance(symbol, interval, limit=1000, start_time=None):
    start_time_ms = int(start_time.timestamp() * 1000) if start_time else 0
    url = BINANCE_BASE_URL.format(
        symbol=symbol,
        interval=interval.lower(),
        limit=limit,
        start_time=start_time_ms)
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