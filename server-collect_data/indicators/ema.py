def calculate_ema(series, span):
    return series.ewm(span=span).mean()