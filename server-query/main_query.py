from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from get_data import get_ohlcv
from shared.symbols_intervals import SYMBOLS, INTERVALS

app = FastAPI()

# streamlit에서 api호출 가능하도록 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 캔들 데이터 호출 api
@app.get("/ohlcv/{symbol}/{interval}")
def read_ohlcv(symbol: str, interval: str):
    data = get_ohlcv(symbol, interval)
    if data is None:
        raise HTTPException(status_code=404, detail="db조회 실패")
    return data
