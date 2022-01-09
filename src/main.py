# import util
# import oanda.client
# import oanda.alpaca_test
import config
from oanda.live import getLiveCerebro
from src.oanda.backtest import getBacktestCerebro
from src.strategy.sample0 import SampleStrategy
import backtrader as bt

from src.strategy.sample1 import TestStrategy

def executeStrategyLive(strategy):
    cerebro = getLiveCerebro()
    cerebro.addstrategy(strategy)
    cerebro.run(exactbars=1)


def backtestStrategy(strategy):
    cerebro = getBacktestCerebro()
    cerebro.addstrategy(strategy)
    cerebro.broker.setcash(100000.0)
    # cerebro.broker.setcommission(commission=0.001)
    print("Value before run", cerebro.broker.getvalue())
    cerebro.run()
    print("Value after run", cerebro.broker.getvalue())
    cerebro.plot()


print("hello world")


backtestStrategy(TestStrategy)
# executeStrategyLive(TestStrategy)

