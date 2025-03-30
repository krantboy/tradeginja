def calculate_momentum(data, periods=10):
    return data['Close'].diff(periods)