# Crypto Trading Bot

An automated cryptocurrency trading bot built in Python that monitors live market data, applies multiple technical analysis strategies, and sends real-time Telegram notifications on every trading decision.

## What It Does

- Connects to Binance testnet for paper trading with fake money
- Fetches live BTC/USDT market data every 5 minutes
- Applies 3 technical analysis strategies simultaneously
- Only trades when all 3 strategies agree — reducing bad trades
- Sends Telegram notifications on every decision
- Logs all activity with timestamps to a local file
- Scans 5 exchanges simultaneously for arbitrage opportunities

## Trading Strategies

### 1. RSI (Relative Strength Index)
Measures momentum on a scale of 0–100.
- Below 40 = oversold → potential BUY
- Above 60 = overbought → potential SELL

### 2. Bollinger Bands
Measures price volatility using upper and lower bands.
- Price below lower band → potential BUY
- Price above upper band → potential SELL

### 3. MACD (Moving Average Convergence Divergence)
Measures momentum shifts using two moving averages.
- MACD above signal line → potential BUY
- MACD below signal line → potential SELL

All 3 strategies must agree before any trade is placed.

## Project Structure
trading-bot/
├── trader.py           # Main bot — automated trading with 3 strategies
├── arbitrage.py        # Multi-exchange arbitrage scanner
├── fetch_price.py      # Live price fetcher with RSI indicator
├── arbitrage_log.txt   # Auto-generated arbitrage activity log
├── trader_log.txt      # Auto-generated trading activity log
├── requirements.txt    # Python dependencies
├── .env                # Secret keys (never pushed to GitHub)
├── .gitignore          # Protects .env from being pushed
└── README.md           # Project documentation

## Tech Stack

- **Python 3.14**
- **CCXT** — unified crypto exchange API library
- **Pandas** — market data manipulation
- **TA (Technical Analysis)** — RSI, Bollinger Bands, MACD calculations
- **Requests** — Telegram API integration
- **python-dotenv** — secure environment variable management

## Exchanges Monitored (Arbitrage)

| Exchange | Status |
|----------|--------|
| Kraken   | Active |
| Coinbase | Active |
| KuCoin   | Active |
| Bybit    | Active |
| OKX      | Active |

## Installation

```bash
# Clone the repository
git clone https://github.com/teejay-ui/Trading-project.git
cd Trading-project

# Install dependencies
pip install ccxt pandas ta requests python-dotenv

# Create .env file with your keys
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
TELEGRAM_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id

# Run the trading bot
python trader.py

# Run the arbitrage scanner
python arbitrage.py
```

## Sample Output
[2026-07-14 02:42:53] Price: $62318.0
[2026-07-14 02:42:53] RSI: 54.21
[2026-07-14 02:42:53] BB Upper: $62437.81 | BB Lower: $61899.09
[2026-07-14 02:42:53] MACD: 9.98 | Signal: -40.3
[2026-07-14 02:42:53] Buy signals: 1/3 | Sell signals: 0/3
[2026-07-14 02:42:53] Balance: 10000.0 USDT | 1.0 BTC | Signal: HOLD
[2026-07-14 02:42:53] No trade executed

## Telegram Notifications

The bot sends a Telegram message on every cycle showing:
- Current price and indicators
- Signal decision (BUY / SELL / HOLD)
- Current balance
- Order details if a trade was placed

## Security

- API keys stored in `.env` file
- `.env` is listed in `.gitignore` and never pushed to GitHub
- Testnet keys used for all paper trading — no real funds at risk

## Deployment

Bot is deployed on Railway for 24/7 cloud execution.

## Disclaimer

This bot is built for educational purposes. It does not use real funds. Always paper trade and understand the strategy fully before using real money.

## Author

**Teejay (Tumba II Z.M. Kongolo)** — Software Engineering Student, African Leadership University  
Cybersecurity enthusiast | Python developer  
[GitHub](https://github.com/teejay-ui)