import os
import sys

import numpy as np

from src.indicators.GradientCoefficient import GradientCoefficient
from src.model.Neural import NeuralNetwork
from src.oanda.live import getLiveCerebro
from src.oanda.backtest import getBacktestCerebro
from src.strategy.NeuralGradient import NeuralGradient

def executeStrategyLive(strategy, params):
    cerebro = getLiveCerebro()
    cerebro.addstrategy(strategy, **params)
    cerebro.run(exactbars=1)


def backtestStrategy(strategy, params):
    startingValue = 1000
    cerebro = getBacktestCerebro()
    cerebro.addstrategy(strategy, **params)
    cerebro.broker.setcash(startingValue)
    cerebro.broker.setcommission(commission=0.0001)
    # print("Value before run", cerebro.broker.getvalue())
    cerebro.run()
    # print("Value after run", cerebro.broker.getvalue())
    # cerebro.plot()
    endingValue = cerebro.broker.getvalue()
    percentageReturn = endingValue / startingValue
    # print("Return for", params, " = ", percentageReturn)
    return percentageReturn

layers = [8, 8, 1]
weights = [
    np.random.rand(8, 8) * 100,
    np.random.rand(1, 8) * 100,
]
activations = [
    np.random.rand(8) / 100, np.random.rand(1) / 100
]

def getIndicators(data):
    return [
        GradientCoefficient(data, n=1),
        GradientCoefficient(data, n=2),
        GradientCoefficient(data, n=3),
        GradientCoefficient(data, n=5),
        GradientCoefficient(data, n=8),
        GradientCoefficient(data, n=13),
        GradientCoefficient(data, n=21),
        GradientCoefficient(data, n=34)
    ]

params = dict(
    network=NeuralNetwork(layers, weights, activations),
    getIndicators=getIndicators
)

print("Start with args", sys.argv)

LIVE = "live"

if sys.argv.__contains__(LIVE):
    print("Executing live")
    executeStrategyLive(NeuralGradient, params)
else:
    print("Executing backtest")
    percentageReturn = backtestStrategy(NeuralGradient, params)
    print("Return is", percentageReturn)

