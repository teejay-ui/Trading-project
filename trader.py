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
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='15m', limit=100)
    df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

    # Strategy 1: RSI
    df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()

    # Strategy 2: Bollinger Bands
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_lower'] = bb.bollinger_lband()

    # Strategy 3: MACD
    macd = ta.trend.MACD(df['close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # Get latest values
    rsi = df['RSI'].iloc[-1]
    price = df['close'].iloc[-1]
    bb_upper = df['BB_upper'].iloc[-1]
    bb_lower = df['BB_lower'].iloc[-1]
    macd_val = df['MACD'].iloc[-1]
    macd_sig = df['MACD_signal'].iloc[-1]

    log(f"Price: ${price}")
    log(f"RSI: {round(rsi, 2)}")
    log(f"BB Upper: ${round(bb_upper, 2)} | BB Lower: ${round(bb_lower, 2)}")
    log(f"MACD: {round(macd_val, 2)} | Signal: {round(macd_sig, 2)}")

    # BUY conditions - all 3 strategies must agree
    rsi_buy = rsi < 40
    bb_buy = price < bb_lower
    macd_buy = macd_val > macd_sig

    # SELL conditions - all 3 strategies must agree
    rsi_sell = rsi > 60
    bb_sell = price > bb_upper
    macd_sell = macd_val < macd_sig

    if rsi_buy and bb_buy and macd_buy:
        return 'BUY', price
    elif rsi_sell and bb_sell and macd_sell:
        return 'SELL', price
    else:
        # Show which strategies agree
        buy_score = sum([rsi_buy, bb_buy, macd_buy])
        sell_score = sum([rsi_sell, bb_sell, macd_sell])
        log(f"Buy signals: {buy_score}/3 | Sell signals: {sell_score}/3")
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
        msg = f"BUY ORDER\nAmount: {amount} BTC\nPrice: ${price}\nBalance: {usdt} USDT"
        log(msg)
        send_telegram(msg)

    elif signal == 'SELL' and btc > 0:
        order = exchange.create_market_sell_order('BTC/USDT', btc)
        msg = f"SELL ORDER\nAmount: {btc} BTC\nPrice: ${price}\nBalance: {usdt} USDT"
        log(msg)
        send_telegram(msg)

    else:
        msg = f"Signal: {signal} | Price: ${price} | No trade executed"
        log("No trade executed")
        send_telegram(msg)

# Bot loop
while True:
    try:
        trade()
        log("-" * 60)
        time.sleep(300)  # Every 5 minutes
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(60)