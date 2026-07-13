import ccxt

exchange = ccxt.binance({
    'apiKey': 'vo3nuIyT9ZIEAO2AR3qNKaE2HKAXapL1HQSLWYeuQwek21vdqIytYcjF8hOqb7XC',
    'secret': 'fhgcRz6JU1LqFU8xtxKcbWRzlLRVwE53aU07KjbIsV29yJUG9cNe79LBhbzwieIt',
})

# Built-in sandbox mode - routes everything to testnet
exchange.set_sandbox_mode(True)

balance = exchange.fetch_balance()
print(f"USDT: {balance['USDT']['free']}")
print(f"BTC: {balance['BTC']['free']}")