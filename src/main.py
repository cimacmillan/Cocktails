# import util
# import oanda.client
# import oanda.alpaca_test
import config
from oanda.live import getLiveCerebro
from src.oanda.backtest import getBacktestCerebro
from src.strategy.sample0 import SampleStrategy
import backtrader as bt

print("hello world")

# cerebro = getLiveCerebro()
cerebro = getBacktestCerebro()
cerebro.addstrategy(SampleStrategy,
                        smaperiod=5,
                        trade=True,
                        exectype=bt.Order.ExecType(bt.Order.ExecTypes[0]),
                        stake=1000,
                        stopafter=0,
                        valid=None,
                        cancel=0,
                        donotcounter=False,
                        sell=False,
                        usebracket=False)

# Live data ... avoid long data accumulation by switching to "exactbars"
# cerebro.run(exactbars=1)

cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)
print(cerebro.broker.getvalue())

cerebro.run()

print(cerebro.broker.getvalue())


