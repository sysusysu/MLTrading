
import numpy as np
import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt


import sys
sys.path.append("../")
from util import get_data, plot_data


def compute_portvals(orders_df, start_val = 1000000, commission=9.95, impact=0.005, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    
    ### read order book, sort it, get start and end date
    orders_df.sort_index(inplace=True)
    start_date = orders_df.index.min() if orders_df.index.min()<sd else sd
    end_date = orders_df.index.max() if orders_df.index.max()>ed else ed
    ### get list of tickers
    tickers = orders_df['Symbol'].unique().tolist()

    df_prices = get_data(tickers, pd.date_range(start_date, end_date))
    df_prices.fillna(method='ffill', inplace=True)
    df_prices.fillna(method='bfill', inplace=True)
    df_prices['cash'] = 1.0

    ### make df_trades
    df_trades = pd.DataFrame(0.0,columns=df_prices.columns,index=df_prices.index)


    ## populate df_trades
    for i in range(orders_df.shape[0]):
        date = orders_df.index[i]
        action = orders_df.iloc[i]["Order"]
        ticker = orders_df.iloc[i]["Symbol"]
        shares = orders_df.iloc[i]["Shares"]
        price = df_prices.loc[date, ticker]
        transaction = shares*price
        if action == "BUY":
            df_trades.loc[date][ticker] += shares
            df_trades.loc[date]['cash'] += -transaction*(1+impact) - commission
        else:
            df_trades.loc[date][ticker] += -shares
            df_trades.loc[date]['cash'] += transaction*(1-impact) - commission
    ## make df_holdings
    df_holdings = pd.DataFrame(0.0,columns=df_prices.columns,index=df_prices.index)
    ## populate df_holdings
    for i in range(df_trades.shape[0]):
        if i ==0:
            df_holdings.iloc[i] = df_trades.iloc[i].copy()
            df_holdings.iloc[i]["cash"] += start_val
        else:
            df_holdings.iloc[i] = df_holdings.iloc[i-1].copy()
            df_holdings.iloc[i] += df_trades.iloc[i]

    ## make df_values
    df_values = pd.DataFrame(0.0,columns=df_prices.columns,index=df_prices.index)
    ## populate df_holdings
    for i in range(df_values.shape[0]):
        date = df_values.index[i]
        df_values.loc[date, 'cash'] = df_holdings.iloc[i]["cash"]
        tmp = df_prices.iloc[i][tickers] * df_holdings.iloc[i][tickers]
        for key in tickers:
            df_values.loc[date, key] = tmp[key]
    df_portval = df_values.sum(axis=1)
    
    
    return df_portval
def get_bench_value(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000,commission=0.0, impact=0.0):
    df_price = get_data([symbol],pd.date_range(sd, ed))
    #print("start date: ", sd)
    dates = [df_price.index[0]]
    actions = ['BUY']
    symbols = [symbol]
    shares = [1000]
    df_order = pd.DataFrame(columns = ['Symbol','Order','Shares'], index = dates)
    df_order['Symbol'] = symbols
    df_order['Order'] = actions
    df_order['Shares'] = shares
    df_v = compute_portvals(df_order, start_val = 100000, sd=sd, ed=ed, commission=commission, impact=impact)
    return(df_v)
    
def assess_portfolio(df_value, bench, names, df_order=None, sf=252.0, rfr=0.0, plot=False):
    merged = pd.concat([df_value, bench], axis=1)
    merged.rename(columns = {0:names[0],1:names[1]}, inplace=True)
    merged = merged.div(merged.iloc[0])  ## normalize stock price to 1 when initializing

    # Get portfolio statistics (note: std_daily_ret = volatility)
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    cr = merged.iloc[-1,:]/merged.iloc[0,:]-1
    daily_r = np.divide(merged.iloc[1:,:].values, merged.iloc[:-1,:].values) - 1
    adr = np.mean(daily_r, axis = 0) 
    sddr = np.std(daily_r, ddof = 1, axis=0)
    sr = np.sqrt(sf)*np.mean(daily_r - rfr, axis=0)/np.std(daily_r - rfr, ddof = 1, axis=0)
    
    ev = merged.iloc[-1,:]*100000
    tmp = []
    tmp.append(['cumulative return', cr[0],cr[1]])
    tmp.append(['average daily return', adr[0],adr[1]])
    tmp.append(['std daily return', sddr[0],sddr[1]])
    tmp.append(['sharpe ratio', sr[0],sr[1]])
    tmp.append(['end value', ev[0],ev[1]])
    result = pd.DataFrame(tmp, columns = ['Measurement']+names)
    if plot:
        plot_two_col(merged, names, df_order=df_order, size = (10,5))
    
    return result
def plot_two_col(data, columns, df_order = None, size = (20,10), perc = 1):
    data = data.sort_index()
    length = data.shape[0]
    start_idx = int((1-perc)*length)

    fig, ax1 = plt.subplots(figsize=size)
    x = data.index[start_idx:]
    
    y1 = data[columns[0]][start_idx:]
    color = "blue" if columns[0]=="Bench" else "black"
    p1, = ax1.plot(x,y1, color=color)
    p1.set_label(columns[0])
    
    y2 = data[columns[1]][start_idx:]
    color = "blue" if columns[1]=="Bench" else "black"
    p2, = ax1.plot(x,y2, color=color)
    p2.set_label(columns[1])
    
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Value')
    ax1.legend()
    #print(df_order)
    if df_order is not None:
        for i in range(df_order.shape[0]):
            c="red"
            if df_order.iloc[i]['Order'] == 'BUY':
                c="green"
            ax1.axvline(x = df_order.index[i],clip_on = True, c = c)


    plt.show()
