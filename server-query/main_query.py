from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from get_data import get_ohlcv
from shared.symbols_intervals import SYMBOLS, INTERVALS
from choi_modified import run_conditional_lateral_backtest, save_result_to_table
from pydantic import BaseModel

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

class StrategyRequest(BaseModel):
    symbol: str
    interval: str
    strategy_sql: str
    risk_reward_ratio: float

@app.post("/save_strategy")
def save_strategy(req: StrategyRequest):
    try:
        result_df = run_conditional_lateral_backtest(
            symbol=req.symbol,
            interval=req.interval,
            strategy_sql=req.strategy_sql,
            risk_reward_ratio=req.risk_reward_ratio
        )
        save_result_to_table(result_df)
        return {"message": "전략 실행 및 결과 저장 완료", "rows": len(result_df)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


