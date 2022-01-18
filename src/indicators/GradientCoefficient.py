import math

import backtrader as bt

class GradientCoefficient(bt.Indicator):
    lines = ('gc',)
    params = (('n', 1),)

    def __init__(self):
        self.addminperiod(self.params.n)

    def next(self):
        diff = (self.data[0] - self.data[-self.p.n])
        # print(diff)
        gradient = diff
        theta = math.atan(gradient)
        # coefficient = math.sin(theta)
        self.lines.gc[0] = theta

        # if coefficient > 1:
        #     print("Unexpected coefficient", coefficient)



