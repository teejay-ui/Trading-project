import ccxt
import time
import pandas as pd
import ta
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

exchange = ccxt.binance({
    'apiKey': os.environ.get('BINANCE_API_KEY'),
    'secret': os.environ.get('BINANCE_SECRET_KEY'),
})

exchange.set_sandbox_mode(True)

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open('trader_log.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def get_signal():
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
    df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

    df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['SMA_10'] = df['close'].rolling(10).mean()
    df['SMA_30'] = df['close'].rolling(30).mean()

    rsi = df['RSI'].iloc[-1]
    sma_10 = df['SMA_10'].iloc[-1]
    sma_30 = df['SMA_30'].iloc[-1]
    price = df['close'].iloc[-1]

    log(f"Price: ${price} | RSI: {round(rsi, 2)} | SMA10: {round(sma_10, 2)} | SMA30: {round(sma_30, 2)}")

    if rsi < 40 and sma_10 > sma_30:
        return 'BUY', price
    elif rsi > 60 and sma_10 < sma_30:
        return 'SELL', price
    else:
        return 'HOLD', price

def get_balance():
    balance = exchange.fetch_balance()
    usdt = balance['USDT']['free']
    btc = balance['BTC']['free']
    return usdt, btc

def trade():
    signal, price = get_signal()
    usdt, btc = get_balance()

    log(f"Balance: {usdt} USDT | {btc} BTC | Signal: {signal}")

    if signal == 'BUY' and usdt > 10:
        amount = round(10 / price, 6)
        order = exchange.create_market_buy_order('BTC/USDT', amount)
        log(f"BUY ORDER PLACED: {amount} BTC at ${price}")
    elif signal == 'SELL' and btc > 0:
        order = exchange.create_market_sell_order('BTC/USDT', btc)
        log(f"SELL ORDER PLACED: {btc} BTC at ${price}")
    else:
        log("No trade executed")

# Bot loop
while True:
    try:
        trade()
        log("-" * 60)
        time.sleep(3600)
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(60)