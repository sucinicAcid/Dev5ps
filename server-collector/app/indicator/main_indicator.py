from config import SYMBOLS, INTERVALS
from db import engine
from indicator.calculator import calculate_indicators
from indicator.crud import update_with_indicators
import pandas as pd

def main():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            tbl = f"{symbol.lower()}_{interval.lower()}"
            query = f"""
                SELECT * FROM {tbl}
                WHERE processed = FALSE AND timestamp < NOW() - INTERVAL '30 seconds'
                ORDER BY timestamp
            """
            df = pd.read_sql(query, con=engine)
            if df.empty:
                continue
            df = calculate_indicators(df)
            update_with_indicators(df, tbl)

if __name__ == "__main__":
    main()