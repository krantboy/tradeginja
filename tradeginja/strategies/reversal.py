import pandas as pd
from ..indicators.rsi import calculate_rsi
from ..indicators.momentum import calculate_momentum
from ..indicators.envelope import calculate_envelope
from ..indicators.knoxville import detect_knoxville_divergence


def detect_reversals(df, rsi_periods=14, momentum_periods=10, ma_period=20, envelope_pct=5, knox_window=5):
    # Calculate indicators
    df['RSI'] = calculate_rsi(df, rsi_periods)
    df['Momentum'] = calculate_momentum(df, momentum_periods)
    df['MA'], df['Upper_Envelope'], df['Lower_Envelope'] = calculate_envelope(df, ma_period, envelope_pct)

    # Knoxville Divergence
    knox_signals = detect_knoxville_divergence(df, df['RSI'], df['Momentum'], knox_window)

    # Envelope Logic
    envelope_signals = pd.Series(index=df.index, dtype='object')
    envelope_signals[(df['Close'].shift(1) > df['Upper_Envelope'].shift(1)) &
                     (df['Close'] < df['Upper_Envelope'])] = 'SELL (Envelope)'
    envelope_signals[(df['Close'].shift(1) < df['Lower_Envelope'].shift(1)) &
                     (df['Close'] > df['Lower_Envelope'])] = 'BUY (Envelope)'

    # Combine signals
    df['Signal'] = knox_signals.fillna(envelope_signals).replace('', pd.NA)
    return df