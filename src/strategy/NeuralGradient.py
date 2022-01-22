import backtrader as bt
import numpy as np

# Create a Stratey
from src.model.Neural import NeuralNetwork

NEURAL_THRESHOLD = 0.5
VOLUME = 10000

class NeuralGradient(bt.Strategy):
    def __init__(self, network: NeuralNetwork, getIndicators):
        self.network = network
        self.indicators = getIndicators(self.datas[0])
        self.buyFeeling = None

    def log(self, text):
        ''' Logging function for this strategy'''
        currentData = self.datas[0]
        currentTime = str(currentData.datetime.date(0)) + " " + str(currentData.datetime.time(0))
        print(currentTime, text)

    def next(self):
        inputs = list(map(
            lambda indicator: indicator[0],
            self.indicators
        ))
        output = self.network.output(np.matrix(inputs))

        if self.buyFeeling is None:
            if output > NEURAL_THRESHOLD:
                self.buyFeeling = True
                self.buy(size=VOLUME/2)
            elif output < -NEURAL_THRESHOLD:
                self.buyFeeling = False
                self.sell(size=VOLUME/2)
            return

        # print("Inputs", inputs)
        # print("Neural Output", self.network.output(np.matrix(inputs)))
        if output > NEURAL_THRESHOLD and self.buyFeeling is False:
            self.buyFeeling = True
            self.buy(size=VOLUME)
        elif output < -NEURAL_THRESHOLD and self.buyFeeling is True:
            self.buyFeeling = False
            self.sell(size=VOLUME)


    def notify_trade(self, trade):
        brokerValue = "$" + str(self.broker.getvalue())
        # self.log("Trade " + str(trade.price) + " " + brokerValue + " " + str(trade.size))
        # print(self.broker.get_fundshares())






