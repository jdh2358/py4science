"""
Download historical pricing record arrays for a universe of stocks
from Yahoo Finance using urllib.  Load them into numpy record arrays
using matplotlib.mlab.csv2rec, and do some batch processing -- make
date vs price charts for each one, and compute the return since 2003
for each stock.  Sort the returns and print out the tickers of the 4
biggest winners
"""
import os, datetime, urllib
import matplotlib.mlab as mlab  # contains csv2rec
import numpy as npy
import pylab as p

def fetch_stock(ticker):
    """
    download the CSV file for stock with ticker and return a numpy
    record array.  Save the CSV file as TICKER.csv where TICKER is the
    stock's ticker symbol.

    Extra credit for supporting a start date and end date, and
    checking to see if the file already exists on the local file
    system before re-downloading it
    """
    fname = '%s.csv'%ticker
    url = 'http://ichart.finance.yahoo.com/table.csv?' +\
   's=%s&d=9&e=20&f=2007&g=d&a=0&b=29&c=1993&ignore=.csv'%ticker

    # the os.path module contains function for checking whether a file
    # exists
    if not os.path.exists(fname):
        urllib.urlretrieve(url, fname)
    r = mlab.csv2rec(fname)

    # note that the CSV file is sorted most recent date first, so you
    # will probably want to sort the record array so most recent date
    # is last
    r.sort()
    return r

tickers = 'SPY', 'QQQQ', 'INTC', 'MSFT', 'YHOO', 'GOOG', 'GE', 'WMT', 'AAPL'

# we want to compute returns since 2003, so define the start date
startdate = datetime.date(2003,1,1)

# we'll store a list of each return and ticker for analysis later
data = []   # a list of (return, ticker) for each stock 
fig = p.figure()
for ticker in tickers:
    print 'fetching', ticker
    r = fetch_stock(ticker)
    
    # select the numpy records where r.date>=startdatre

    r = r[r.date>=startdate]
    price = r.adj_close                 # set price equal to the adjusted close
    returns = (price-price[0])/price[0] # return is the (price-p0)/p0
    data.append((returns[-1], ticker))  # store the data

    # plot the returns by date for each stock
    p.plot(r.date, returns, label=ticker)

p.legend(loc='upper left')

# now sort the data by returns and print the results for each stock
data.sort()
for g, ticker in data:
    print '%s: %1.1f%%'%(ticker, 100*g)


p.savefig('stock_records.png', dpi=100)
p.savefig('stock_records.eps')
p.show()
