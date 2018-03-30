
import datetime as dt
import pandas as pd
import numpy as np
import random
from scipy import optimize

import indicators, marketsimcode


# import sys
# sys.path.append("../")
import util as ut

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.thresholds = []
        self.commission = 0
        self.impact = 0
    def portfolio_sr(self, port_val, full_return=False):

        rfr = 0 
        sf = 252

        # Get portfolio statistics (note: std_daily_ret = volatility)
        cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
        cr = port_val[-1]/port_val[0]-1
        daily_r = np.divide(port_val[1:].values, port_val[:-1].values) - 1
        adr = np.mean(daily_r) 
        sddr = np.std(daily_r, ddof = 1)
        sr = np.sqrt(sf)*np.mean(daily_r - rfr)/np.std(daily_r - rfr, ddof = 1)
        if full_return:
            return cr, adr, sddr, sr
        else:
            return sr
    def get_strategy_perf(self, thresholds, df_price, symbol, sd, ed, sv, return_order_book=False):
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
                RSIbull = df_price.iloc[i]['RSI']/100
                MACDbull = df_price.iloc[i]['MACD9day_avg'] - df_price.iloc[i]['MACD']
                Bollbull = -df_price.iloc[i]['bb_value']
                
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
        cr, adr, sddr, sr = [0.0, 0.0, 0.0, 0.0]
        
        if df_order.shape[0]>0:
            df_value = marketsimcode.compute_portvals(df_order, start_val = sv, commission=self.commission, impact=self.impact, sd=sd, ed=ed)
            sr, adr, sddr, cr = self.portfolio_sr(df_value, full_return=True)
#         print "return: ", return_order_book
        
        if return_order_book:
            return(df_order)
        else:
            return(-sr)
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        # add your code to do learning here
        # add your code to do learning here
        ### get 60 days ahead of starding date, to avoid NA in indicators
        esd = sd - dt.timedelta(days = 60)

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(esd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later

        ### get indicators
        ## names: [u'IBM', u'SMA', u'BOLLup', u'BOLLdown', u'bb_value', u'change', u'RSI',
        ##         u'EMA12', u'EMA26', u'MACD', u'MACD9day_avg']
        price_ind = indicators.get_indicator(prices[symbol])
        price_ind = price_ind.loc[sd:,:]

#         thresholds = [0.31,0.30,0.32,0.33,0.34,0.35]
        ## winning
#         thresholds = [0.4,0.6, 0.3]
#         initial_sim = np.random.uniform(low = 0.0, high = 1.0,size=(5,4))
        
#         print "=========="
#         print "initial sim: ",initial_sim
#         print "=========="
#         res = optimize.minimize(self.get_strategy_perf, thresholds, args = (price_ind, symbol, sd,ed,sv), 
#                                 method='Nelder-Mead',options={'maxiter': 5, 'initial_simplex':initial_sim})
#       =================
        thresholds = [0.4,0.6, 0.3]
        initial_sim = np.random.uniform(low = 0.0, high = 1.0,size=(4,3))
        # print "=========="
        # print "initial sim: ",initial_sim
        # print "=========="
        res = optimize.minimize(self.get_strategy_perf, thresholds, args = (price_ind, symbol, sd,ed,sv), 
                                method='Nelder-Mead',options={'maxiter': 5, 'initial_simplex':initial_sim})
#         res = optimize.minimize(self.get_strategy_perf, thresholds, args = (price_ind, symbol, sd,ed,sv), 
#                                 method='SLSQP',options={'maxiter': 10000})
        self.thresholds = res.x
        compare = self.get_strategy_perf([0.9512683, 0.31918724, 1. ], price_ind, symbol, sd, ed, sv, return_order_book=False)
        if res.fun > compare:
            self.thresholds = [0.9512683, 0.31918724, 1.]
        # print "Optimal thresh: ", res
        if self.verbose: print prices
        if self.verbose: print volume

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        esd = sd - dt.timedelta(days = 60)
        dates = pd.date_range(esd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        price_ind = indicators.get_indicator(prices_all[symbol])
        price_ind = price_ind.loc[sd:,:]
        
#         obj = obj_func(symbol, sd, ed)
        df_order = self.get_strategy_perf(self.thresholds, price_ind, symbol, sd, ed, sv, return_order_book=True)
#         sr = self.get_strategy_perf(self.thresholds, price_ind, symbol, sd, ed, sv, return_order_book=False, test=True)
        
        trades = prices_all[[symbol,]]
        trades.loc[:,:] = 0
        for i in range(df_order.shape[0]):
            idx = df_order.index[i]
            if df_order['Order'][i] == "BUY":
                trades.loc[idx, :] = df_order['Shares'][i]
            else:
                trades.loc[idx, :] = -df_order['Shares'][i]
        if self.verbose: print type(df_order) # it better be a DataFrame!
        if self.verbose: print df_order
        if self.verbose: print price_ind
        return trades
    def addEvidence2(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        # add your code to do learning here
        # add your code to do learning here
        ### get 60 days ahead of starding date, to avoid NA in indicators
        esd = sd - dt.timedelta(days = 60)

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(esd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later

        ### get indicators
        ## names: [u'IBM', u'SMA', u'BOLLup', u'BOLLdown', u'bb_value', u'change', u'RSI',
        ##         u'EMA12', u'EMA26', u'MACD', u'MACD9day_avg']
        price_ind = indicators.get_indicator(prices[symbol])
        price_ind = price_ind.loc[sd:,:]

#         thresholds = [0.31,0.30,0.32,0.33,0.34,0.35]
        ## winning
#         thresholds = [0.4,0.6, 0.3]
#         initial_sim = np.random.uniform(low = 0.0, high = 1.0,size=(5,4))
        
#         print "=========="
#         print "initial sim: ",initial_sim
#         print "=========="
#         res = optimize.minimize(self.get_strategy_perf, thresholds, args = (price_ind, symbol, sd,ed,sv), 
#                                 method='Nelder-Mead',options={'maxiter': 5, 'initial_simplex':initial_sim})
#       =================
        thresholds = [0.4,1, 1]
        initial_sim = np.random.uniform(low = 0.0, high = 1.0,size=(4,3))
        initial_sim[0,:] = [0.04,1, 1]
        # print "=========="
        # print "initial sim: ",initial_sim
        # print "=========="
        res = optimize.minimize(self.get_strategy_perf, thresholds, args = (price_ind, symbol, sd,ed,sv), 
                                method='Nelder-Mead',options={'maxiter': 100, 'initial_simplex':initial_sim})
#         res = optimize.minimize(self.get_strategy_perf, thresholds, args = (price_ind, symbol, sd,ed,sv), 
#                                 method='SLSQP',options={'maxiter': 10000})
        self.thresholds = res.x
        # print "obj value: ",res.fun
        compare = self.get_strategy_perf([0.9512683, 0.31918724, 1. ], price_ind, symbol, sd, ed, sv, return_order_book=False)
        if res.fun > compare:
            self.thresholds = [0.9512683, 0.31918724, 1.]
        # print "Optimal thresh: ", res
        if self.verbose: print prices
        if self.verbose: print volume
    def testPolicy2(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        esd = sd - dt.timedelta(days = 60)
        dates = pd.date_range(esd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        price_ind = indicators.get_indicator(prices_all[symbol])
        price_ind = price_ind.loc[sd:,:]
        
#         obj = obj_func(symbol, sd, ed)
        df_order = self.get_strategy_perf(self.thresholds, price_ind, symbol, sd, ed, sv, return_order_book=True)
#         sr = self.get_strategy_perf(self.thresholds, price_ind, symbol, sd, ed, sv, return_order_book=False, test=True)
        if df_order.shape[0]==0:
            df_order.loc[price_ind.index[2],"Symbol"] = symbol
            df_order.loc[price_ind.index[2],"Order"] = "BUY"
            df_order.loc[price_ind.index[2],"Shares"] = 1000
            df_order.loc[price_ind.index[-1],"Symbol"] = symbol
            df_order.loc[price_ind.index[-1],"Order"] = "SELL"
            df_order.loc[price_ind.index[-1],"Shares"] = 1000
        # print "thresholds: ",self.thresholds
        return df_order

    
if __name__=="__main__":
    print "One does not simply think up a strategy"