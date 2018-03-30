
"""Analyze a portfolio."""
from __future__ import division
import pandas as pd
import numpy as np
import datetime as dt

#import sys
#sys.path.append("..")
from util import get_data, plot_data





def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1),     syms = ['GOOG','AAPL','GLD','XOM'],     allocs=[0.1,0.2,0.3,0.4],     sv=1000000, rfr=0.0, sf=252.0,     gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices_all.fillna(method='ffill', inplace=True)
    prices_all.fillna(method='bfill', inplace=True)
    prices_all = prices_all.div(prices_all.iloc[0])  ## normalize stock price to 1 when initializing
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    # add code here to compute daily portfolio values
    tmp = prices.multiply(allocs, axis = 1)
    port_val = tmp.sum(axis = 1)
    port_real_val = port_val.multiply(sv)

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    cr = port_val[-1]/port_val[0]-1
    daily_r = np.divide(port_val[1:].values, port_val[:-1].values) - 1
    adr = np.mean(daily_r) 
    sddr = np.std(daily_r, ddof = 1)
    sr = np.sqrt(sf)*np.mean(daily_r - rfr)/np.std(daily_r - rfr, ddof = 1)
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp)

    # Add code here to properly compute end value
    ev = port_real_val[-1]
    return cr, adr, sddr, sr, ev

def test_code():
    
    start_date = dt.datetime(2007,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['FAKE1','FAKE2']
    allocations = [0.5, 0.5]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,        syms = symbols,         allocs = allocations,        sv = start_val,         gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr




if __name__ == "__main__":
    test_code()






