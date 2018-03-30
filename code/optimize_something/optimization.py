
# coding: utf-8

# In[2]:


"""MC1-P2: Optimize a portfolio."""
from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from scipy import optimize

#import sys
#sys.path.append("..")
from util import get_data, plot_data



# In[98]:


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality


#### assess volatility of portfolio. 
def portfolio_metrics(allocs, prices, full_return = False):
    
    rfr = 0 
    sf = 252
    
    # add code here to compute daily portfolio values
    tmp = prices.multiply(allocs, axis = 1)
    port_val = tmp.sum(axis = 1)

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    cr = port_val[-1]/port_val[0]-1
    daily_r = np.divide(port_val[1:].values, port_val[:-1].values) - 1
    adr = np.mean(daily_r) 
    sddr = np.std(daily_r, ddof = 1)
    sr = np.sqrt(sf)*np.mean(daily_r - rfr)/np.std(daily_r - rfr, ddof = 1)
    if full_return:
        return port_val, cr, adr, sddr, sr
    else:
        return sddr



def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices_all.fillna(method='ffill', inplace=True) ## fill nan
    prices_all.fillna(method='bfill', inplace=True)
    prices_all = prices_all.div(prices_all.iloc[0])  ## normalize stock price to 1 when initializing

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    ### initialite allocations
    allocs = np.asarray([1.0/len(syms)]*len(syms)) # add code here to find the allocations

    ### optimize
    cons = ({'type': 'eq', 'fun': lambda x:  1 - np.sum(x)})
    bnds=[(0,1)]*len(syms)
    res = optimize.minimize(portfolio_metrics, allocs, args = prices, method='SLSQP', bounds=bnds, constraints=cons)

    solution = res.x
    port_val, cr, adr, sddr, sr = portfolio_metrics(solution, prices, full_return = True)


    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title='Daily Portfolio Value and SPY')

    return solution, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,        syms = symbols,         gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr


# In[99]:


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()








