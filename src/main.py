import os

# import util
# import oanda.client
# import oanda.alpaca_test
from src.oanda.live import getLiveCerebro
from src.oanda.backtest import getBacktestCerebro
import backtrader as bt

from src.strategy.sample1 import TestStrategy

def executeStrategyLive(strategy):
    cerebro = getLiveCerebro()
    cerebro.addstrategy(strategy)
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

params = dict(
    sma=2
)
percentageReturn = backtestStrategy(TestStrategy, params)
print("Return for", params, " = ", percentageReturn)

# print("hello world")
# bestPercentage = None
# bestIndex = None
#
# for i in range(1, 100):
#     params = dict(
#         sma=i
#     )
#     percentageReturn = backtestStrategy(TestStrategy, params)
#     print("Return for", params, " = ", percentageReturn)
#
#     if bestPercentage is None or percentageReturn > bestPercentage:
#         bestPercentage = percentageReturn
#         bestIndex = i
#         print("Best SMA ", i)

# executeStrategyLive(TestStrategy)

