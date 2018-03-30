
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



import sys
sys.path.append("../")
from util import get_data


## indicators = ['SMA', 'BOLL', 'RSI', 'KDJ']
def weight_avg(data, k):
    return(data[1]*k+data[0]*(1-k))
    
    
def get_indicator(stock_data):
    name = stock_data.name
    data = pd.DataFrame(stock_data.values, columns = [stock_data.name], index = stock_data.index)
    ## sort index
    data.sort_index(inplace=True)
    
    ## calculate SMA
    sma_days = 21
    data['SMA'] = data[name].rolling(window=sma_days).mean()
    
    ## calculate BOLL
    rolling_std = data[name].rolling(window=sma_days).std()
    data['BOLLup'] = data['SMA'] + rolling_std *2
    data['BOLLdown'] = data['SMA'] - rolling_std *2
    # bb_value[t] = (price[t] - SMA[t])/(2 * stdev[t])
    data['bb_value'] = (data[name]-data['SMA'])/2/rolling_std
    ## bb_value sma
    data['bb_value9day_avg'] = data['bb_value'].rolling(window=9).mean()
    ## bb_value diff
    data['bb_value_diff'] = data['bb_value'] - data['bb_value9day_avg']
    ## RSI
    rsi_day = 12
    data['change'] = np.nan
    data['change'][1:] = data[name].values[1:] - data[name].values[0:-1]

    up = data['change'].where(data['change']>=0).fillna(0)
    down = np.absolute(data['change'].where(data['change']<0)).fillna(0)
    cumup = up.rolling(rsi_day).sum()
    cumdown = down.rolling(rsi_day).sum()
    rs = (cumup/rsi_day)/(cumdown/rsi_day)
    data['RSI'] = 100.0 - 100.0/(1+rs)
    data.loc[rs==np.inf, 'RSI'] = 100.0
    ## sma of RSI
    data['RSI9day_avg'] = data['RSI'].rolling(window=9).mean()
    ## MACD
    k = 2.0/(12+1)
    sma12 = data[name].rolling(window=12).mean()
    data['EMA12'] = sma12.rolling(window=2).apply(weight_avg, args=[k])
    
    k = 2.0/(26+1)
    sma26 = data[name].rolling(window=26).mean()
    data['EMA26'] = sma26.rolling(window=2).apply(weight_avg, args=[k])
    data['MACD'] = data['EMA12'] - data['EMA26']
    
    data['MACD9day_avg'] = data['MACD'].rolling(window=9).mean()
    return(data)
def author():
    return 'xxx'



