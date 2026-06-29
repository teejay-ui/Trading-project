import ccxt
import time
from datetime import datetime

kraken = ccxt.kraken()

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open('arbitrage_log.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def check_arbitrage():
    # Compare BTC/USD vs BTC/USDT on Kraken
    btc_usd = kraken.fetch_ticker('BTC/USD')['last']
    btc_usdt = kraken.fetch_ticker('BTC/USDT')['last']

    spread = btc_usd - btc_usdt

    log(f"BTC/USD: ${btc_usd} | BTC/USDT: ${btc_usdt} | Spread: ${round(spread, 2)}")

    if spread > 10:
        log("OPPORTUNITY FOUND: Buy BTC/USDT, Sell BTC/USD on Kraken")
    elif spread < -10:
        log("OPPORTUNITY FOUND: Buy BTC/USD, Sell BTC/USDT on Kraken")
    else:
        log("No opportunity right now")

# Bot loop
while True:
    try:
        check_arbitrage()
        time.sleep(5)
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(10)