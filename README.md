# postgreSQL db 초기화
docker-compose down
docker-compose up --build db
python delete_all_data.py

docker-compose down
docker-compose up --build

# 메커니즘
[ Binance API ]
      ↓
[ server-collect_data ]
    - 데이터 수집
    - RSI, EMA, MACD 계산
    - PostgreSQL에 저장
      ↓
[ server-analyze_data ]
    - 조건 조합 필터링 (예: RSI < 30 and MACD > 0)
    - 결과 따로 저장 (Filtered Timeframe)
