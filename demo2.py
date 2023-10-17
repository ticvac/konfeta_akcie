from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import pandas as pd

aapl_data = pd.read_csv("MCS.csv")
aapl_data["Close"] = aapl_data["Close"].apply(lambda x : float(str(x)[1:]))
aapl_data["Open"] = aapl_data["Open"].apply(lambda x : float(str(x)[1:]))
aapl_data["Low"] = aapl_data["Low"].apply(lambda x : float(str(x)[1:]))
aapl_data["High"] = aapl_data["High"].apply(lambda x : float(str(x)[1:]))

GOOG = GOOG.tail(700)

aapl_data = aapl_data.reindex(index=aapl_data.index[::-1])
aapl_data.reset_index(inplace=True, drop=True)
aapl_data = aapl_data.tail(700)

#aapl_data = aapl_data.reindex(index=aapl_data.index[::-1])
#aapl_data.reset_index(inplace=True, drop=True)

print(GOOG)
print(aapl_data)

print("----- a ----")

class SmaCross(Strategy):
    # pro aap 11, 
    n1 = 9
    n2 = 11

    shortN = 2
    longN = 60
    offset = 15
    volumeDiff = 0

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)
        self.last_close = self.data.Close[0]     
        print("--a--")
        #self.vI = self.I(self.calculate_volume_diff)
        #self.smaS = self.I(SMA, close, self.shortN)
        #self.smaL = self.I(SMA, close, self.longN)
        #self.trashUp = self.I(self.calculate_offset_by)
        #self.offset = -self.offset
        #self.trashDown = self.I(self.calculate_offset_by)
        self.var = self.I(self.calculate_varS)

    def calculate_varS(self):
        return pd.Series(self.data.Close).rolling(252).var()

    
    def calculate_volume_diff(self):
        last_close = 0
        volume_diff = -self.data.Close[0]
        volume_indicator = []

        for i in range(len(self.data.Close)):
            if self.data.Close[i] > last_close:
                volume_diff += self.data.Volume[i]
            else:
                volume_diff -= self.data.Volume[i]
            last_close = self.data.Close[i]
            volume_indicator.append(volume_diff)

        for i in range(len(volume_indicator)):
            volume_indicator[i] /= 100000
        return volume_indicator
    
    def calculate_offset_by(self):
        my_values = []
        
        for i in self.smaL.data:
            my_values.append(i + self.offset)
        return my_values
            
    bought_on = 0
    log = []

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()
        return

        if self.smaS[-1] + 2 < self.bought_on:
            self.sell()
            self.log.append(["sell safa", self.data.Close[-1]])

        if crossover(self.smaS, self.trashUp):
            print("i - ze spoda")
        if crossover(self.trashUp, self.smaS):
            print("i - ze shora")
            self.sell()
            self.log.append(["sell profit", self.data.Close[-1]])

        if crossover(self.smaS, self.trashDown):
            print("j - ze spodu")
            self.log.append(["buy low", self.data.Close[-1]])
            self.buy()
            self.bought_on = self.data.Close[-1]
        if crossover(self.trashDown, self.smaS):
            print("j - ze shora")

        


bt = Backtest(aapl_data, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True, trade_on_close=False)

#a = bt.optimize(offset = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],)
#a = bt.optimize(n1=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], n2=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
#                  constraint=lambda p: p.n1 < p.n2)



output = bt.run()
bt.plot()

print(a)
print(type(a))
print(a._strategy)