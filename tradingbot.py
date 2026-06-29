import ccxt

exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
})

# Fetch real-time BTC/USDT price
ticker = exchange.fetch_ticker('BTC/USDT')
print(f"Current BTC Price: {ticker['last']}")

# Fetch OHLCV candle data for analysis
ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
print(ohlcv)