import abc

class Notifier(abc.ABC):
    """Base class for all notification types."""
    @abc.abstractmethod
    def notify(self, subject: str, body: str):
        """Send a notification with a subject and body."""
        pass

def notify_new_signals(df, notifier: Notifier, ticker: str):
    """Notify about new signals using the provided notifier."""
    new_signals = df[df['Signal'].notna()]
    if new_signals.empty:
        return

    body = f"New reversal signals detected for {ticker}:\n\n"
    for _, row in new_signals.iterrows():
        body += f"Date: {row['Date']}, Close: {row['Close']:.2f}, Signal: {row['Signal']}\n"
    subject = f"Tradeginja Alert: New Reversal Signals for {ticker}"
    notifier.notify(subject, body)