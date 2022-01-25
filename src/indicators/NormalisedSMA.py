import math

import backtrader as bt

class NormalisedSMA(bt.Indicator):
    lines = ('sma',)
    params = (('period', 20),)

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        current = self.data[0]
        sma = math.fsum(self.data.get(size=self.p.period)) / self.p.period
        normalisedSMA = (current - sma) * 1e4
        self.lines.sma[0] = normalisedSMA



