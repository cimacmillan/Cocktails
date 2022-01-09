from datetime import datetime

from src.config import getOandaKeys
import backtrader as bt
import btoandav20

data0Label = "GBP_USD"
broker = True

StoreCls = btoandav20.stores.OandaV20Store

def getBacktestCerebro():
    [account, token] = getOandaKeys()

    cerebro = bt.Cerebro(oldbuysell=True)

    store = StoreCls(
        token=token,
        account=account,
        practice=True
    )

    # broker = store.getbroker()
    # cerebro.setbroker(broker)

    DataFactory = store.getdata

    data0 = DataFactory(
        dataname=data0Label,
        timeframe=bt.TimeFrame.Minutes,
        fromdate=datetime(2022, 1, 1),
        historical=True,
    )
    cerebro.adddata(data0)

    return cerebro
