import backtrader as bt

# Create a Stratey
class TestStrategy(bt.Strategy):

    def __init__(self):
        self.shortSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=1)
        self.longSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=3)
        self.shortGreater = None


    def log(self, text):
        ''' Logging function for this strategy'''
        currentData = self.datas[0]
        currentTime = str(currentData.datetime.date(0)) + str(currentData.datetime.time(0))
        print(currentTime, text)


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close ' + str(self.datas[0].close[0]))
        self.log('Short SMA ' + str(self.shortSMA[0]))
        self.log('Long SMA ' + str(self.longSMA[0]))
        if self.shortGreater is None:
            self.shortGreater = self.shortSMA[0] > self.longSMA[0]
        elif self.shortGreater is True and self.longSMA[0] > self.shortSMA[0]:
            self.sell(
                size=100
            )
            self.shortGreater = False
        elif self.shortGreater is False and self.longSMA[0] < self.shortSMA[0]:
            self.buy(
                size=100
            )
            self.shortGreater = True


    def notify_trade(self, trade):
        brokerValue = "$" + str(self.broker.getvalue())
        self.log("Trade " + str(trade.price) + " " + brokerValue)




