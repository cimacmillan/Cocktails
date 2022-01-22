from datetime import datetime

from ..config import getOandaKeys
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
    fromdate=datetime(2022, 1, 16),
    todate=datetime(2022, 1, 18),
    historical=True,
)

def getBacktestCerebro():
    cerebro = bt.Cerebro(oldbuysell=True)
    cerebro.adddata(data0)
    return cerebro
