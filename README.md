# Tradeginja

A Python package for detecting trends in stock tickers using technical indicators like RSI, Knoxville Divergence, and Moving Average Envelopes. 

### Prerequisites
- Python 3.7+

### Clone the Repository
This is a private repo (`https://github.com/krantboy/tradeginja.git`), so you need to authenticate:

#### Using HTTPS with PAT
1. Generate a PAT (GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic), `repo` scope).
2. Clone:
   ```bash
   git clone https://krantboy:<your-pat>@github.com/krantboy/tradeginja.git
   ```

#### Using SSH
1. Set up SSH (`ssh-keygen -t ed25519`, add public key to GitHub > Settings > SSH and GPG keys).
2. Clone:
   ```bash
   git clone git@github.com:krantboy/tradeginja.git
   ```

### Install the Package
```bash
cd tradeginja
pip install -e .
```

## Running the Script

The `detect_reversals.py` script is the main tool for analyzing stock tickers. It fetches data from Yahoo Finance, detects reversals, saves results to CSV files, and optionally sends email notifications for new signals. Run it from the `tradeginja/` directory.

### Basic Command
```bash
python tradeginja/scripts/detect_reversals.py --tickers AAPL
```
- Processes AAPL for the last 180 days (default), saves to `stock_data_aapl.csv` and `signals_aapl.csv`.

### Setting Up Email Notifications
To enable email notifications without typing credentials each time, use environment variables:

1. **Set Environment Variables**:
   ```bash
   export TRADEGINJA_SENDER_EMAIL="your_email@gmail.com"
   export TRADEGINJA_RECEIVER_EMAIL="your_email@gmail.com"
   export TRADEGINJA_EMAIL_PASSWORD="your_app_password"
   ```
   - Replace with your email and app-specific password (e.g. https://myaccount.google.com/apppasswords).
   - Make permanent by adding to `~/.bashrc` or `~/.zshrc` and running `source ~/.bashrc`.
   - Do not use your original gmail password :) 

2. **Run with Email**:
   ```bash
   python tradeginja/scripts/detect_reversals.py --tickers AAPL TSLA
   ```
   - Sends emails for new signals using the stored credentials.

### Usage Examples

1. **Single Ticker**:
   ```bash
   python tradeginja/scripts/detect_reversals.py --tickers AAPL
   ```
   - Output: Signals for AAPL, files `stock_data_aapl.csv` and `signals_aapl.csv`.

2. **Multiple Tickers**:
   ```bash
   python tradeginja/scripts/detect_reversals.py --tickers AAPL TSLA MSFT
   ```
   - Output: Signals for each ticker, files like `stock_data_tsla.csv`, `signals_msft.csv`.

3. **Custom Date Range**:
   ```bash
   python tradeginja/scripts/detect_reversals.py --tickers AAPL TSLA --days-back 90 --end-date "2025-04-01"
   ```
   - Analyzes 90 days ending April 1, 2025.

4. **Custom Output Files**:
   ```bash
   python tradeginja/scripts/detect_reversals.py --tickers AAPL --data-key "my_data.csv" --signal-key "my_signals.csv"
   ```
   - Saves to `my_data_aapl.csv` and `my_signals_aapl.csv`.

5. **Override Email Settings (Optional)**:
   ```bash
   python tradeginja/scripts/detect_reversals.py --tickers AAPL TSLA --sender-email "other_email@gmail.com" --receiver-email "other_receiver@gmail.com" --email-password "other_password"
   ```
   - Overrides environment variables if provided.

### Output
- **Console**: Prints signals (e.g., Date, Close, Signal) for each ticker.
- **Files**: 
  - `stock_data_<ticker>.csv`: Full data per ticker.
  - `signals_<ticker>.csv`: Detected signals per ticker.
- **Email**: Sent for new signals (if email vars are set), one per ticker with signal details.

### Command-Line Options
- `--tickers`: Ticker symbols (required, e.g., `AAPL TSLA`).
- `--days-back`: Days of data to fetch (default: 180).
- `--end-date`: End date (default: 2025-03-29, format: YYYY-MM-DD).
- `--data-key`: Base filename for data (default: stock_data.csv).
- `--signal-key`: Base filename for signals (default: signals.csv).
- `--sender-email`: Sender email (default: `$TRADEGINJA_SENDER_EMAIL`).
- `--receiver-email`: Receiver email (default: `$TRADEGINJA_RECEIVER_EMAIL`).
- `--email-password`: Email password (default: `$TRADEGINJA_EMAIL_PASSWORD`).

## Troubleshooting
- **No Output**: Ensure Python and dependencies (`yfinance`, `pandas`, `numpy`) are installed.
- **No Signals**: Delete old `signals_*.csv` files or adjust `--days-back` for recent data.
- **Email Not Working**: Verify environment variables and use an app-specific password for Gmail.