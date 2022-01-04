from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream
from .keys import ALPACA_SECRET, ALPACA_PUBLIC, ALPACA_URL

api = REST(
    key_id=ALPACA_PUBLIC,
    secret_key=ALPACA_SECRET,
    base_url=ALPACA_URL
)
print(api.get_bars("AAPL", TimeFrame.Hour, "2021-12-01", "2021-12-01", adjustment='raw').df)


async def trade_callback(t):
    api.submit_order(
        symbol="AAPL",
        qty=1
    )
    print('trade', t)


async def quote_callback(q):
    print('quote', q)


# Initiate Class Instance
stream = Stream(
        key_id=ALPACA_PUBLIC,
        secret_key=ALPACA_SECRET,
        base_url=ALPACA_URL,
        data_feed='iex')  # <- replace to SIP if you have PRO subscription

# subscribing to event
stream.subscribe_trades(trade_callback, 'AAPL')
# stream.subscribe_quotes(quote_callback, 'AAPL')

stream.run()