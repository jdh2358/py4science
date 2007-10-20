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
    url = XXX # create the url for this ticker

    # the os.path module contains function for checking whether a file
    # exists, and fetch it if not
    XXX

    # load the CSV file intoo a numpy record array
    r = XXX

    # note that the CSV file is sorted most recent date first, so you
    # will probably want to sort the record array so most recent date
    # is last
    XXX
    return r

tickers = 'INTC', 'MSFT', 'YHOO', 'GOOG', 'GE', 'WMT', 'AAPL'

# we want to compute returns since 2003, so define the start date as a
# datetime.datetime instance
startdate = XXX

# we'll store a list of each return and ticker for analysis later
data = []   # a list of (return, ticker) for each stock 
fig = p.figure()
for ticker in tickers:
    print 'fetching', ticker
    r = fetch_stock(ticker)
    
    # select the numpy records where r.date>=startdatre use numpy mask
    # indexing to restrict r to just the dates > startdate
    r = XXX
    price = XXX   # set price equal to the adjusted close
    returns = XXX # return is the (price-p0)/p0
    XXX           # store the data

    # plot the returns by date for each stock using pylab.plot, adding
    # a label for the legend
    XXX

# use pylab legend command to build a legend
XXX

# now sort the data by returns and print the results for each stock
XXX

# show the figures
p.show()
