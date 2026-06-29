import ccxt
import pandas as pd
import ta

exchange = ccxt.binance()

# Fetch candle data (OHLCV = Open, High, Low, Close, Volume)
ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)

# Load into a dataframe
df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

# Convert timestamp to readable time
df['time'] = pd.to_datetime(df['time'], unit='ms')

# Add RSI indicator
df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()

# Show last 10 rows
print(df[['time', 'close', 'RSI']].tail(10))