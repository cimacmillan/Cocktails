import os
import sys

import numpy as np

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

layers = [1, 1, 1]
weights = np.matrix([
    [1], [1]
])
activations = np.matrix([
    [1], [1], [1]
])

params = dict(
    network=NeuralNetwork(layers, weights, activations)
)

print("Start with args", sys.argv)

LIVE = "live"

if sys.argv.__contains__(LIVE):
    print("Executing live")
    executeStrategyLive(NeuralGradient, params)
else:
    print("Executing backtest")
    percentageReturn = backtestStrategy(NeuralGradient, params)
    print("Return for", params, " = ", percentageReturn)

