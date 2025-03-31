def calculate_envelope(data, ma_period=20, envelope_pct=5):
    ma = data['Close'].rolling(window=ma_period).mean()
    upper_band = ma * (1 + envelope_pct / 100)
    lower_band = ma * (1 - envelope_pct / 100)
    return ma, upper_band, lower_band