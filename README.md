# Crypto Arbitrage Trading Bot

A Python-based cryptocurrency arbitrage bot that monitors price differences across multiple exchanges in real-time and identifies profit opportunities.

## What It Does

- Connects to 5 major crypto exchanges simultaneously (Kraken, Coinbase, KuCoin, Bybit, OKX)
- Fetches live BTC/USDT prices from each exchange every 5 seconds
- Calculates price spreads across all exchanges
- Identifies arbitrage opportunities when spread exceeds $20
- Logs every check with timestamps to a local file

## How Arbitrage Works

Arbitrage exploits price differences for the same asset across different markets. If BTC is selling for $60,100 on Bybit and $60,050 on KuCoin, you can buy on KuCoin and sell on Bybit for a $50 profit per BTC.

## Tech Stack

- **Python 3.14**
- **CCXT** — unified crypto exchange API library
- **Pandas** — market data manipulation
- **TA (Technical Analysis)** — RSI and indicator calculations

## Exchanges Monitored

| Exchange | Status |
|----------|--------|
| Kraken   | Active |
| Coinbase | Active |
| KuCoin   | Active |
| Bybit    | Active |
| OKX      | Active |

## Project Structure
trading-bot/
├── arbitrage.py        # Main bot — multi-exchange arbitrage scanner
├── fetch_price.py      # Price fetcher with RSI indicator
├── arbitrage_log.txt   # Auto-generated log of all bot activity
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

## Installation

```bash
# Clone the repository
git clone https://github.com/teejay-ui/Trading-project.git
cd Trading-project

# Install dependencies
pip install -r requirements.txt

# Run the bot
python arbitrage.py
```

## Sample Output
[2026-06-29 11:15:46] kraken: $59949.0
[2026-06-29 11:15:46] coinbase: $59960.0
[2026-06-29 11:15:46] kucoin: $59955.0
[2026-06-29 11:15:46] bybit: $59900.0
[2026-06-29 11:15:46] okx: $59890.0
[2026-06-29 11:15:46] Best spread: $70.0 | Buy on okx ($59890.0) | Sell on coinbase ($59960.0)
[2026-06-29 11:15:46] OPPORTUNITY FOUND: Buy on okx, Sell on coinbase | Profit: $70.0

## Deployment

Bot is deployed on Railway for 24/7 cloud execution.

## Disclaimer

This bot is built for educational purposes. It does not execute real trades. Always paper trade and understand the strategy fully before using real funds.

## Author

**Teejay** — Software Engineering Student, African Leadership University  
Cybersecurity enthusiast | Python developer  
[GitHub](https://github.com/teejay-ui)
