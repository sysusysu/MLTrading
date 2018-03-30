
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


import sys
sys.path.append("../")
from util import get_data


class BestPossibleStrategy(object):
    
    #### best strategy
    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df_price = get_data([symbol],pd.date_range(sd, ed))
        #print(df_price.shape)
        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0
        for i in range(0, df_price.shape[0]):
            if i+1<df_price.shape[0]:
                ## sell 
                if df_price.iloc[i][symbol] > df_price.iloc[i+1][symbol]:
                    if net == 0:
                        shares.append(1000)
                        dates.append(df_price.index[i])
                        actions.append('SELL')
                        symbols.append(symbol)
                        net=-1000
                    elif net == 1000:
                        shares.append(2000)
                        dates.append(df_price.index[i])
                        actions.append('SELL')
                        symbols.append(symbol)
                        net=-1000
                    elif net == -1000:
                        continue
                ## buy
                elif df_price.iloc[i][symbol] < df_price.iloc[i+1][symbol]:

                    if net == 0:
                        shares.append(1000)
                        dates.append(df_price.index[i])
                        actions.append('BUY')
                        symbols.append(symbol)
                        net = 1000
                    elif net == -1000:
                        shares.append(2000)
                        dates.append(df_price.index[i])
                        actions.append('BUY')
                        symbols.append(symbol)
                        net = 1000
                    elif net == 1000:
                        continue
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbols
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return(df_order)



