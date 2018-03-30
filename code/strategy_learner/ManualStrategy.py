
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import indicators
import os

import sys
sys.path.append("../")
from util import get_data

class ManualStrategy(object):
    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df_price = get_data([symbol],pd.date_range(sd, ed))
        df_indicators = indicators.get_indicator(df_price[symbol])

        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0

        for i in range(0, df_price.shape[0]):
            if i+1<df_price.shape[0]:
                ## buy
                if df_indicators.iloc[i]['RSI'] < 20:
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
                elif df_indicators.iloc[i]['RSI'] >80:
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
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbols
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return(df_order)
    def testRSIs(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df_price = get_data([symbol],pd.date_range(sd, ed))
        df_indicators = indicators.get_indicator(df_price[symbol])

        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0

        for i in range(0, df_price.shape[0]):
            if i+1<df_price.shape[0]:
                ## buy
                if df_indicators.iloc[i]['RSI'] < df_indicators.iloc[i]['RSI9day_avg']:
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
                elif df_indicators.iloc[i]['RSI'] > df_indicators.iloc[i]['RSI9day_avg']:
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
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbols
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return(df_order)
    def testMACD(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df_price = get_data([symbol],pd.date_range(sd, ed))
        df_indicators = indicators.get_indicator(df_price[symbol])

        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0

        for i in range(0, df_price.shape[0]):

            if i+1<df_price.shape[0]:
                ## buy
                if df_indicators.iloc[i]['MACD'] < df_indicators.iloc[i]['MACD9day_avg'] :
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
                ## sell
                elif df_indicators.iloc[i]['MACD'] > df_indicators.iloc[i]['MACD9day_avg'] :
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
            else:
                if net == 1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('SELL')
                    symbols.append(symbol)
                    net=0
                elif net == -1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('BUY')
                    symbols.append(symbol)
                    net=0
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbols
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return(df_order)
    def testBoll(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df_price = get_data([symbol],pd.date_range(sd, ed))
        df_indicators = indicators.get_indicator(df_price[symbol])

        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0

        for i in range(0, df_price.shape[0]):

            if i+1<df_price.shape[0]:
                ## buy
                if df_indicators.iloc[i]['bb_value'] < -0.5 :
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
                ## sell
                elif df_indicators.iloc[i]['bb_value'] > 0.5 :
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
            else:
                if net == 1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('SELL')
                    symbols.append(symbol)
                    net=0
                elif net == -1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('BUY')
                    symbols.append(symbol)
                    net=0
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbols
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return(df_order)
    def testBoll2(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df_price = get_data([symbol],pd.date_range(sd, ed))
        df_indicators = indicators.get_indicator(df_price[symbol])

        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0

        for i in range(0, df_price.shape[0]):

            if i+1<df_price.shape[0] and i >0:
                diff = df_indicators.iloc[i]['bb_value_diff'] - df_indicators.iloc[i-1]['bb_value_diff']
                ## buy
                if diff > 0.2:
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
                ## sell
                elif diff < -0.3 :  # good: 0.3
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
            else:
                if net == 1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('SELL')
                    symbols.append(symbol)
                    net=0
                elif net == -1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('BUY')
                    symbols.append(symbol)
                    net=0
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbols
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return(df_order)
    def test_combined(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df_price = get_data([symbol],pd.date_range(sd, ed))
        df_indicators = indicators.get_indicator(df_price[symbol])

        thresholds = [-0.28226175,  0.80310596,  0.05925771, -0.4072101 ,  0.95184508, -0.84624115]
        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0
        for i in range(0, df_price.shape[0]):
            RSIbull = 1    # true: 1, false: -1, neutral: 0
            MACDbull = 1
            Bollbull = 1
            if i+1<df_price.shape[0]:
                if df_indicators.iloc[i]['RSI'] < thresholds[0]*100:
                    RSIbull = 1
                elif df_indicators.iloc[i]['RSI'] >thresholds[1]*100:
                    RSIbull = -1
                # else:
                #     RSIbull = 0

                if df_indicators.iloc[i]['MACD'] < df_indicators.iloc[i]['MACD9day_avg'] - thresholds[2]:
                    MACDbull = 1
                elif df_indicators.iloc[i]['MACD'] > df_indicators.iloc[i]['MACD9day_avg'] + thresholds[3]:
                    MACDbull = -1
                # else:
                #     MACDbull = 0

                if df_indicators.iloc[i]['bb_value'] < thresholds[4]:
                    Bollbull = 1
                elif df_indicators.iloc[i]['bb_value'] > thresholds[5]:
                    Bollbull = -1
                # else:
                #     Bollbull = 0
                ## make decision
                sum_bull = RSIbull + MACDbull + Bollbull
                ## buy
                if sum_bull >= 2:
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
                ## short
                elif sum_bull <= -2:
                    if net == 0:
                        shares.append(1000)
                        dates.append(df_price.index[i])
                        actions.append('SELL')
                        symbols.append(symbol)
                        net = -1000
                    elif net == 1000:
                        shares.append(2000)
                        dates.append(df_price.index[i])
                        actions.append('SELL')
                        symbols.append(symbol)
                        net = -1000
                    elif net == -1000:
                        continue
                # ## empty
                # else:
                #     if net == 0:
                #         continue
                #     elif net == 1000:
                #         shares.append(1000)
                #         dates.append(df_price.index[i])
                #         actions.append('SELL')
                #         symbols.append(symbol)
                #         net = 0
                #     elif net == -1000:
                #         shares.append(1000)
                #         dates.append(df_price.index[i])
                #         actions.append('BUY')
                #         symbols.append(symbol)
                #         net = 0
            else:
                if net == 1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('SELL')
                    symbols.append(symbol)
                    net=0
                elif net == -1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('BUY')
                    symbols.append(symbol)
                    net=0
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbol
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return df_order
    def test_combined2(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        
        esd = sd - dt.timedelta(days = 60)
        df_price = get_data([symbol],pd.date_range(esd, ed))
        df_indicators = indicators.get_indicator(df_price[symbol])
        df_price = df_price.loc[sd:, :]
        df_indicators = df_indicators.loc[sd:, :]

        # thresholds = [ 0.9512683  , 0.31918724 , 1. ]
        thresholds = [0.4,  1. ,         1. ]

        dates = []
        actions = []
        symbols = []
        shares = []
        net = 0
        rsibulls =[]
        macdbulls = []
        bollbulls = []
        for i in range(0, df_price.shape[0]):
            RSIbull = 1.0    # true: 1, false: -1, neutral: 0
            MACDbull = 1.0
            Bollbull = 1.0
            if i+1<df_price.shape[0]:
                RSIbull = df_indicators.iloc[i]['RSI']/100
                MACDbull = df_indicators.iloc[i]['MACD9day_avg'] - df_indicators.iloc[i]['MACD']
                Bollbull = -df_indicators.iloc[i]['bb_value']
                
                rsibulls.append(RSIbull)
                macdbulls.append(MACDbull)
                bollbulls.append(Bollbull)

#                 else:
#                     Bollbull = 0
                ## make decision
                sum_bull = thresholds[0]*RSIbull + thresholds[1]*MACDbull + thresholds[2]*Bollbull
                ## buy
                if sum_bull >= 2:
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
                ## sell
                elif sum_bull <= -2:
                    if net == 0:
                        shares.append(1000)
                        dates.append(df_price.index[i])
                        actions.append('SELL')
                        symbols.append(symbol)
                        net = -1000
                    elif net == 1000:
                        shares.append(2000)
                        dates.append(df_price.index[i])
                        actions.append('SELL')
                        symbols.append(symbol)
                        net = -1000
                    elif net == -1000:
                        continue
            else:
                if net == 1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('SELL')
                    symbols.append(symbol)
                    net=0
                elif net == -1000:
                    shares.append(1000)
                    dates.append(df_price.index[i])
                    actions.append('BUY')
                    symbols.append(symbol)
                    net=0
#         print "Max RSI: ", np.max(rsibulls), ", min: ",np.min(rsibulls)
#         print "Max MACD: ", np.max(macdbulls), ", min: ",np.min(macdbulls) 
#         print "Max Boll: ", np.max(bollbulls), ", min: ",np.min(bollbulls) 
        df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
        df_order['Symbol'] = symbols
        df_order['Order'] = actions
        df_order['Shares'] = shares
        return df_order




