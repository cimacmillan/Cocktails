from datetime import datetime

from src.config import getOandaKeys
import backtrader as bt
import btoandav20

data0Label = "GBP_USD"

StoreCls = btoandav20.stores.OandaV20Store

[account, token] = getOandaKeys()

store = StoreCls(
    token=token,
    account=account,
    practice=True
)

DataFactory = store.getdata

data0 = DataFactory(
    dataname=data0Label,
    timeframe=bt.TimeFrame.Minutes,
    fromdate=datetime(2022, 1, 6),
    historical=True,
)

def getBacktestCerebro():

    cerebro = bt.Cerebro(oldbuysell=True)

    # broker = store.getbroker()
    # cerebro.setbroker(broker)

    cerebro.adddata(data0)

    return cerebro
