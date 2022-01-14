import backtrader as bt

# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('sma', 160),
    )

    def __init__(self):
        # self.shortSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=8)
        # self.longSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.sma)
        self.shortGreater = None


    def log(self, text):
        ''' Logging function for this strategy'''
        currentData = self.datas[0]
        currentTime = str(currentData.datetime.date(0)) + " " + str(currentData.datetime.time(0))
        print(currentTime, text)

    wait = 0
    inter = 1000
    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close ' + str(self.datas[0].close[0]))
        # self.log('Short SMA ' + str(self.shortSMA[0]))
        # self.log('Long SMA ' + str(self.longSMA[0]))
        volume = 1
        self.wait = (self.wait + 1) % self.inter
        print(self.wait)
        if self.wait == 1:
            self.buy(size=volume)
            print("Buying")
        elif self.wait == self.inter / 2:
            self.sell(size=volume)
            print("Selling")




    def notify_trade(self, trade):
        brokerValue = "$" + str(self.broker.getvalue())
        self.log("Trade " + str(trade.price) + " " + brokerValue)
        # print(self.broker.get_fundshares())






