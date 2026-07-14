import ccxt
import time
import pandas as pd
import ta
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

exchange = ccxt.binance({
    'apiKey': os.environ.get('BINANCE_API_KEY'),
    'secret': os.environ.get('BINANCE_SECRET_KEY'),
})

exchange.set_sandbox_mode(True)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

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
        msg = f"BUY ORDER PLACED\nAmount: {amount} BTC\nPrice: ${price}\nBalance: {usdt} USDT"
        log(msg)
        send_telegram(msg)

    elif signal == 'SELL' and btc > 0:
        order = exchange.create_market_sell_order('BTC/USDT', btc)
        msg = f"SELL ORDER PLACED\nAmount: {btc} BTC\nPrice: ${price}\nBalance: {usdt} USDT"
        log(msg)
        send_telegram(msg)

    else:
        msg = f"No trade executed\nSignal: {signal}\nPrice: ${price}\nRSI: "
        log("No trade executed")
        send_telegram(msg)

# Bot loop
while True:
    try:
        trade()
        log("-" * 60)
        time.sleep(3600)
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(60)