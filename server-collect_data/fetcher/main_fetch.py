import time
from shared.config import SYMBOLS, INTERVALS
from fetcher.fetch_ohlcv import save_to_db

def main_loop(interval_seconds=60):
    while True:
        start_time = time.time()

        for symbol in SYMBOLS:
            for interval in INTERVALS:
                try:
                    print(f"{symbol}_{interval} → 저장 시작")
                    save_to_db(symbol, interval)
                except Exception as e:
                    print(f"{symbol}_{interval} 저장 중 오류 발생: {e}")

        elapsed = time.time() - start_time
        sleep_time = max(0, interval_seconds - elapsed)

        print(f"루프 소요 시간: {elapsed:.2f}초 → 다음 루프까지 {sleep_time:.2f}초 대기\n")

        time.sleep(sleep_time)



if __name__ == "__main__":
    main_loop(interval_seconds=60)
