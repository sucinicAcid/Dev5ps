def calculate_volume_ma(series, span):
    return series.rolling(window=span).mean()