import ccxt
import time
from datetime import datetime

# Connect to all exchanges
exchanges = {
    'kraken': ccxt.kraken(),
    'coinbase': ccxt.coinbase(),
    'kucoin': ccxt.kucoin(),
    'bybit': ccxt.bybit(),
    'okx': ccxt.okx(),
}

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open('arbitrage_log.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def get_prices():
    prices = {}
    for name, exchange in exchanges.items():
        try:
            ticker = exchange.fetch_ticker('BTC/USDT')
            prices[name] = ticker['last']
        except Exception as e:
            log(f"Error fetching {name}: {e}")
    return prices

def check_arbitrage():
    prices = get_prices()

    if len(prices) < 2:
        log("Not enough exchange data")
        return

    # Find cheapest and most expensive
    cheapest = min(prices, key=prices.get)
    expensive = max(prices, key=prices.get)

    spread = prices[expensive] - prices[cheapest]

    # Print all prices
    for name, price in prices.items():
        log(f"{name}: ${price}")

    log(f"Best spread: ${round(spread, 2)} | Buy on {cheapest} (${prices[cheapest]}) | Sell on {expensive} (${prices[expensive]})")

    if spread > 20:
        log(f"OPPORTUNITY FOUND: Buy on {cheapest}, Sell on {expensive} | Profit: ${round(spread, 2)}")
    else:
        log(f"No opportunity right now | Best spread: ${round(spread, 2)}")

    log("-" * 60)

# Bot loop
while True:
    try:
        check_arbitrage()
        time.sleep(5)
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(10)