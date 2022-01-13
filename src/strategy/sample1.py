import backtrader as bt

# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('sma', 160),
    )

    def __init__(self):
        self.shortSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=8)
        self.longSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.sma)
        self.shortGreater = None


    def log(self, text):
        ''' Logging function for this strategy'''
        currentData = self.datas[0]
        currentTime = str(currentData.datetime.date(0)) + " " + str(currentData.datetime.time(0))
        print(currentTime, text)


    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close ' + str(self.datas[0].close[0]))
        # self.log('Short SMA ' + str(self.shortSMA[0]))
        # self.log('Long SMA ' + str(self.longSMA[0]))
        volume = 10000
        if self.shortGreater is None:
            self.shortGreater = self.shortSMA[0] > self.longSMA[0]
            if self.shortGreater is True:
                self.close()
                self.buy(
                    size=volume
                )
            elif self.shortGreater is False:
                self.close()
                self.sell(
                    size=volume
                )
        elif self.shortGreater is True and self.longSMA[0] > self.shortSMA[0]:
            self.close()
            self.sell(
                size=volume
            )
            self.shortGreater = False
        elif self.shortGreater is False and self.longSMA[0] < self.shortSMA[0]:
            self.close()
            self.buy(
                size=volume
            )
            self.shortGreater = True



    def notify_trade(self, trade):
        brokerValue = "$" + str(self.broker.getvalue())
        self.log("Trade " + str(trade.price) + " " + brokerValue)
        # print(self.broker.get_fundshares())






