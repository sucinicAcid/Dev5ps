import pandas as pd
import numpy as np
from sqlalchemy import text
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from shared.connect_db import engine
from shared.symbols_intervals import SYMBOLS, INTERVALS


# symbol_interval 테이블에서 OHLCV 데이터를 조회하고 반환
def get_ohlcv(symbol: str, interval: str):

    if symbol not in SYMBOLS or interval not in INTERVALS:
        return JSONResponse(
            content={"error": "테이블이 존재하지 않습니다."}, status_code=400
        )

    table_name = f"{symbol.lower()}_{interval}"
    query = text(f"SELECT * FROM {table_name} ORDER BY timestamp")

    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    if df.empty:
        return JSONResponse(content=[], status_code=200)

    # 필요한 데이터만 추출
    columns_to_keep = ["timestamp", "open", "high", "low", "close", "volume"]
    df = df[columns_to_keep]

    # NaN, inf, -inf 제거 처리
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.where(pd.notnull(df), None)
    df = df.astype(object)

    # DataFrame을 리스트 딕셔너리로 변환 후 FastAPI가 인식할 수 있도록 jsonable_encoder로 변환 후 JSON 응답 반환
    safe_data = jsonable_encoder(df.to_dict(orient="records"))
    return JSONResponse(content=safe_data)
