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



def getBacktestCerebro():
    data0 = DataFactory(
        dataname=data0Label,
        timeframe=bt.TimeFrame.Minutes,
        fromdate=datetime(2022, 1, 17),
        todate=datetime(2022, 1, 18),
        historical=True,
    )
    cerebro = bt.Cerebro(oldbuysell=True, maxcpus=None)
    cerebro.adddata(data0)
    return cerebro
