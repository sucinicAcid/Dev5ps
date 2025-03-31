def compute_ema(series, span):
    return series.ewm(span=span).mean()