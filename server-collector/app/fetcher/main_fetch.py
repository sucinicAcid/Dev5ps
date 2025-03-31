from shared.config import SYMBOLS, INTERVALS
from fetcher.crud import save_to_db

def main():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                save_to_db(symbol, interval)
            except Exception as e:
                print(f"Error saving {symbol}_{interval}: {e}")

if __name__ == "__main__":
    main()
