import yfinance as yf
import pandas as pd
import argparse
import os
from datetime import datetime, timedelta


def detect_reversals_in_ticker(tickers, start_date, end_date, storage,
                               data_key: str, signal_key: str, notifier=None,
                               **reversal_kwargs):
    from tradeginja.strategies.reversal import detect_reversals
    from tradeginja.notifications import notify_new_signals

    tickers = [tickers] if isinstance(tickers, str) else tickers
    results = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            if df.empty:
                print(f"No data retrieved for {ticker}")
                continue
            df = df.reset_index()
            # Convert Date to UTC to avoid mixed time zones
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            df = detect_reversals(df, **reversal_kwargs)

            ticker_data_key = f"{data_key.rsplit('.', 1)[0]}_{ticker.lower()}.{data_key.rsplit('.', 1)[1]}"
            ticker_signal_key = f"{signal_key.rsplit('.', 1)[0]}_{ticker.lower()}.{signal_key.rsplit('.', 1)[1]}"

            prev_signals = storage.load(ticker_signal_key)
            # Ensure prev_signals Date is also UTC
            if not prev_signals.empty:
                prev_signals['Date'] = pd.to_datetime(prev_signals['Date'], utc=True)
            storage.save(df, ticker_data_key)

            if not prev_signals.empty:
                new_signals = df[df['Signal'].notna() & ~df['Date'].isin(prev_signals['Date'])]
            else:
                new_signals = df[df['Signal'].notna()]

            print(f"New signals for {ticker}: {len(new_signals)} rows")
            if not new_signals.empty:
                print(f"Saving signals to {ticker_signal_key}")
                if notifier:
                    print(f"Attempting to send email for {ticker}")
                    notify_new_signals(new_signals, notifier, ticker)
                signals = df[df['Signal'].notna()]
                storage.save(signals, ticker_signal_key)
                print(f"Saved {len(signals)} signals to {ticker_signal_key}")
            else:
                print(f"No new signals for {ticker} - no file saved")

            results[ticker] = df
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return results if len(results) > 1 else next(iter(results.values()), None)


def main():
    parser = argparse.ArgumentParser(description="Detect reversals in stock tickers using Tradeginja.")
    parser.add_argument("--tickers", nargs="+", required=True, help="Ticker symbols (e.g., AAPL TSLA)")
    parser.add_argument("--days-back", type=int, default=180, help="Days back from end date (default: 180)")
    parser.add_argument("--end-date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="End date (YYYY-MM-DD, default: today)")
    parser.add_argument("--data-key", type=str, default="stock_data.csv",
                        help="Base filename for data (default: stock_data.csv)")
    parser.add_argument("--signal-key", type=str, default="signals.csv",
                        help="Base filename for signals (default: signals.csv)")
    parser.add_argument("--sender-email", type=str, default=os.getenv("TRADEGINJA_SENDER_EMAIL"),
                        help="Sender email (default: $TRADEGINJA_SENDER_EMAIL)")
    parser.add_argument("--receiver-email", type=str, default=os.getenv("TRADEGINJA_RECEIVER_EMAIL"),
                        help="Receiver email (default: $TRADEGINJA_RECEIVER_EMAIL)")
    parser.add_argument("--email-password", type=str, default=os.getenv("TRADEGINJA_EMAIL_PASSWORD"),
                        help="Email password (default: $TRADEGINJA_EMAIL_PASSWORD)")

    args = parser.parse_args()

    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=args.days_back)
    from tradeginja.storage import CSVStorage
    from tradeginja.notifications import EmailNotifier
    storage = CSVStorage(base_path=".")

    notifier = None
    if args.sender_email and args.receiver_email and args.email_password:
        notifier = EmailNotifier(
            sender_email=args.sender_email,
            receiver_email=args.receiver_email,
            password=args.email_password
        )
        print(f"Notifier initialized with sender: {args.sender_email}")
    else:
        print("Email notifications skipped: missing sender-email, receiver-email, or email-password")

    result = detect_reversals_in_ticker(
        args.tickers, start_date, end_date, storage, args.data_key, args.signal_key, notifier=notifier
    )
    if result is not None:
        if isinstance(result, dict):
            for ticker, df in result.items():
                print(f"\n{ticker} Signals:")
                print(df[df['Signal'].notna()][['Date', 'Close', 'Signal']])
        else:
            print(f"\n{args.tickers[0]} Signals:")
            print(result[result['Signal'].notna()][['Date', 'Close', 'Signal']])


if __name__ == "__main__":
    main()