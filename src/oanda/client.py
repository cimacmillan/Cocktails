import time

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
    global positions
    # print('trade', t)
    if (len(positions) <= 0):
        print("I have no positions... Better buy a share of APPL")
        api.submit_order(
            symbol="AAPL",
            qty=1,
            side="buy"
        )
        positions = api.list_positions()
        return

    applePosition = positions[0]
    avgBuy = float(applePosition.avg_entry_price)
    quantity = float(applePosition.qty)
    profit = (t.price - avgBuy) * quantity
    print("I own", quantity, "shares in apple. Each are worth", avgBuy, ". I've made $", profit)

    if quantity < 0:
        print("I am short... Going to buy lots now")
        api.submit_order(
            symbol="AAPL",
            qty=-quantity,
            side="buy"
        )
        positions = api.list_positions()
        return

    if quantity == 0:
        print("I have no shares...")
        return

    if profit > 0.01:
        print("profit is greater than 50 cents so I'm gunna sell")
        api.submit_order(
            symbol="AAPL",
            qty=quantity,
            side="sell"
        )
        positions = api.list_positions()

    if profit < -1:
        print("im losing big, drop this")
        api.submit_order(
            symbol="AAPL",
            qty=quantity,
            side="sell"
        )
        positions = api.list_positions()



async def quote_callback(q):
    print('quote', q)


# Initiate Class Instance
stream = Stream(
        key_id=ALPACA_PUBLIC,
        secret_key=ALPACA_SECRET,
        base_url=ALPACA_URL,
        data_feed='iex')  # <- replace to SIP if you have PRO subscription

# subscribing to event
# stream.subscribe_quotes(quote_callback, 'AAPL')

print("buying tendies")

api.submit_order(
    symbol="AAPL",
    qty=1,
    side="buy"
)

time.sleep(3)

positions = api.list_positions()
print("Current positions", positions)

# api.submit_order(
#     symbol="AAPL",
#     qty=1,
#     side="sell"
# )

stream.subscribe_trades(trade_callback, 'AAPL')



stream.run()