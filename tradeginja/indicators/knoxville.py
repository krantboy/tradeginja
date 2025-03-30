import pandas as pd

def detect_knoxville_divergence(df, rsi, momentum, window=5):
    df['Price_High'] = df['Close'].rolling(window=window).max()
    df['Price_Low'] = df['Close'].rolling(window=window).min()
    df['Mom_High'] = momentum.rolling(window=window).max()
    df['Mom_Low'] = momentum.rolling(window=window).min()

    signals = pd.Series(index=df.index, dtype='object')
    signals[(df['Close'] > df['Price_High'].shift(1)) &
            (momentum < df['Mom_High'].shift(1)) &
            (rsi > 70)] = 'SELL (Knoxville)'
    signals[(df['Close'] < df['Price_Low'].shift(1)) &
            (momentum > df['Mom_Low'].shift(1)) &
            (rsi < 30)] = 'BUY (Knoxville)'
    return signals