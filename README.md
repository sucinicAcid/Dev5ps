docker-compose down
docker-compose up --build collect_data

docker-compose down
docker-compose up --build


# 서버 구분

Dev5ps/
│
├── server-collect_data/    # FastAPI 없이 실행하는 서버
│   └── app/
│        ├── models.py
│        ├── config.py
│        ├── db.py
│        ├── requirements.txt
│        ├── Dockerfile
│        ├── fetcher/                    # 1. Binance에서 데이터 수집 및 저장
│        │      ├── binance_client.py
│        │      ├── crud.py
│        │      └── main_fetch.py           # 수집 및 저장 엔트리포인트
│        └── indicator/                  # 2. 보조지표 계산 후 DB 업데이트
│               ├── rsi.py
│               ├── ema.py
│               ├── macd.py
│               ├── bollinger.py
│               ├── calculator.py           # 전체 지표 계산 모듈
│               ├── crud.py
│               └── main_indicator.py       # 지표 계산 실행 엔트리포인트
├── server-api/                  # 프론트엔드에 API 제공 (조건 캔들, 차트 등)
│   ├── app/
│   │   ├── routers/
│   │   │   ├── charts.py         # 개별 차트 요청 API
│   │   │   └── timeframes.py     # 조건 만족 타임프레임 목록 API
│   │   ├── schemas.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── shared/                      # 공통 유틸리티 및 DB 모듈
│   ├── db.py                    # DB 연결 (SQLAlchemy)
│   ├── config.py
│   └── utils.py
├── frontend/                    # Streamlit 기반 UI
│   ├── src/
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
├── .env.collector
├── .env.analyzer
├── .env.api
├── docker-compose.yml
└── README.md

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
