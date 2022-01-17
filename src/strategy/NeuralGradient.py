import backtrader as bt
import numpy as np

# Create a Stratey
from src.model.Neural import NeuralNetwork


class NeuralGradient(bt.Strategy):
    def __init__(self, network):
        self.network = network

    def log(self, text):
        ''' Logging function for this strategy'''
        currentData = self.datas[0]
        currentTime = str(currentData.datetime.date(0)) + " " + str(currentData.datetime.time(0))
        print(currentTime, text)


    # def next(self):
    #     # print("")

    def notify_trade(self, trade):
        brokerValue = "$" + str(self.broker.getvalue())
        # self.log("Trade " + str(trade.price) + " " + brokerValue)
        # print(self.broker.get_fundshares())






