import backtrader as bt
import datetime

class SampleStrategy(bt.Strategy):
    params = dict(
        smaperiod=5,
        trade=False,
        stake=10,
        exectype=bt.Order.Market,
        stopafter=0,
        valid=None,
        cancel=0,
        donotcounter=False,
        sell=False,
        usebracket=False,
    )

    def __init__(self):
        # To control operation entries
        self.orderid = list()
        self.order = None

        self.counttostop = 0
        self.datastatus = 0

        # Create SMA on 2nd data
        self.sma = bt.indicators.MovAv.SMA(self.data, period=self.p.smaperiod)

        print('--------------------------------------------------')
        print('Strategy Created')
        print('--------------------------------------------------')

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        # Only runs on live data
        if status == data.LIVE:
            self.counttostop = self.p.stopafter
            self.datastatus = 1

    def notify_store(self, msg, *args, **kwargs):
        print('*' * 5, 'STORE NOTIF:', msg)

    def notify_order(self, order):
        if order.status in [order.Completed, order.Cancelled, order.Rejected]:
            self.order = None

        print('-' * 50, 'ORDER BEGIN', datetime.datetime.now())
        print(order)
        print('-' * 50, 'ORDER END')

    def notify_trade(self, trade):
        print('-' * 50, 'TRADE BEGIN', datetime.datetime.now())
        print(trade)
        print('-' * 50, 'TRADE END')

    def prenext(self):
        self.next(frompre=True)

    def next(self, frompre=False):
        txt = list()
        txt.append('Data0')
        txt.append('%04d' % len(self.data0))
        dtfmt = '%Y-%m-%dT%H:%M:%S.%f'
        txt.append('{:f}'.format(self.data.datetime[0]))
        txt.append('%s' % self.data.datetime.datetime(0).strftime(dtfmt))
        txt.append('{:f}'.format(self.data.open[0]))
        txt.append('{:f}'.format(self.data.high[0]))
        txt.append('{:f}'.format(self.data.low[0]))
        txt.append('{:f}'.format(self.data.close[0]))
        txt.append('{:6d}'.format(int(self.data.volume[0])))
        txt.append('{:d}'.format(int(self.data.openinterest[0])))
        txt.append('{:f}'.format(self.sma[0]))
        print(', '.join(txt))

        if len(self.datas) > 1 and len(self.data1):
            txt = list()
            txt.append('Data1')
            txt.append('%04d' % len(self.data1))
            dtfmt = '%Y-%m-%dT%H:%M:%S.%f'
            txt.append('{}'.format(self.data1.datetime[0]))
            txt.append('%s' % self.data1.datetime.datetime(0).strftime(dtfmt))
            txt.append('{}'.format(self.data1.open[0]))
            txt.append('{}'.format(self.data1.high[0]))
            txt.append('{}'.format(self.data1.low[0]))
            txt.append('{}'.format(self.data1.close[0]))
            txt.append('{}'.format(self.data1.volume[0]))
            txt.append('{}'.format(self.data1.openinterest[0]))
            txt.append('{}'.format(float('NaN')))
            print(', '.join(txt))

        if self.counttostop:  # stop after x live lines
            self.counttostop -= 1
            if not self.counttostop:
                self.env.runstop()
                return

        if not self.p.trade:
            return

        if self.datastatus and not self.position and len(self.orderid) < 1:
            if not self.p.usebracket:
                if not self.p.sell:
                    # price = round(self.data0.close[0] * 0.90, 2)
                    price = self.data0.close[0] - 0.005
                    self.order = self.buy(size=self.p.stake,
                                          exectype=self.p.exectype,
                                          price=price,
                                          valid=self.p.valid)
                else:
                    # price = round(self.data0.close[0] * 1.10, 4)
                    price = self.data0.close[0] - 0.05
                    self.order = self.sell(size=self.p.stake,
                                           exectype=self.p.exectype,
                                           price=price,
                                           valid=self.p.valid)

            else:
                print('USING BRACKET')
                price = self.data0.close[0] - 0.05
                self.order, _, _ = self.buy_bracket(size=self.p.stake,
                                                    exectype=bt.Order.Market,
                                                    price=price,
                                                    stopprice=price - 0.10,
                                                    limitprice=price + 0.10,
                                                    valid=self.p.valid)

            self.orderid.append(self.order)
        elif self.position and not self.p.donotcounter:
            if self.order is None:
                if not self.p.sell:
                    self.order = self.sell(size=self.p.stake // 2,
                                           exectype=bt.Order.Market,
                                           price=self.data0.close[0])
                else:
                    self.order = self.buy(size=self.p.stake // 2,
                                          exectype=bt.Order.Market,
                                          price=self.data0.close[0])

            self.orderid.append(self.order)

        elif self.order is not None and self.p.cancel:
            if self.datastatus > self.p.cancel:
                self.cancel(self.order)

        if self.datastatus:
            self.datastatus += 1

    def start(self):
        if self.data0.contractdetails is not None:
            print('-- Contract Details:')
            print(self.data0.contractdetails)

        header = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume',
                  'OpenInterest', 'SMA']
        print(', '.join(header))

        self.done = False
