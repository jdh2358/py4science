"""
Use urllib to download key statistics for several stock tickers; URL example pattern

http://finance.yahoo.com/q/ks?s=INTC
"""

import datetime, time  
import urllib
import os
import BeautifulSoup

XXX = None
def get_datadir():
    """
    return the data dir used by this program.  It should be
    data/key_stats.  use the "os" module to check for the directories existence and create it if
    necessary.  See os.exists, os.path.join and os.mkdir
    """
    XXX
    return datadir

def grab_data(tickers):
    """
    download the html file for each ticker in the list of tickers and
    put the output into datadir with a filename like
    'GOOG_key_stats.html'.  Look at urllib.urlretrieve for fetching
    the file over the web, and insert a time.sleep command in between
    each file grab to lower the burden on the server.

    Return value is a list of (ticker,
    pathname) where pathname is a path to the html file. 
    """
    datadir = get_datadir()
    datafiles = []
    for ticker in tickers:
        # make an output filename be creating a file like
        # "GOOG_key_stats.html" in the datadir
        fname = XXX

        # only download the file if it doesn't already exist.  Since these
        # stats can change daily, in real life we might want to put a date
        # stamp on the files too
        if not os.path.exists(fname):
            # build the URL from the format pattern and ticker and grab it with urllib
            # use time.sleep between grabs to be gentle on the server
            XXX
            print 'fetched %s into %s'%(ticker, fname)
        else:
            print 'already have', fname
        datafiles.append((ticker, fname))
    return datafiles


def convert(x):
    """
    The table data is all strings and we want to convert it to python
    datatypes as intelligently as possible.  For serios use, you would
    want converters depending on the column header, but where we'll
    just inspect the string and try and do something semi-intelligent.
    Eg, if it ends with '%', strip the '%' and return a float.  If it
    ends with 'M', strip the 'M' and multipl by 1e6 (likewise for 'K'
    and 'B').  Try to convert things that look like dates to
    python.date objects using time.strptime and datetime.date.  Try
    and convert to float using a try/except block.  If everything
    fails, just return the string
    """
    XXX
    return x

def parse_htmlfile(fname):
    """
    parse the key statistics html in fname and return a data
    dictionary.  The keys are the headers, and the values are the
    converted data items
    """

    # beautiful soup lets you filter html tags by their properties.  I
    # took a peak at one of the html sources and found the tags that
    # correspond to the tables, headers and dataitems we are interested
    # in.  Yahoo was nice enough to put "class" information in the tags
    # which makes this particularly easy.  We'll use the table props, the
    # headerprops and the dataprops to select out just the tables and
    # table elements we want
    tableprops  = {'class': 'yfnc_datamodoutline1'}
    headerprops = {'class': 'yfnc_tablehead1'}
    dataprops   = {'class': 'yfnc_tabledata1'}

    # create the beautiful soup instance with the html string
    soup = BeautifulSoup.BeautifulSoup(file(fname).read())
    datad = dict()
    for table in soup('table', **tableprops): # get all the data tables
        for row in table('tr'):               # iterate over all rows
            XXX # get the header and data items and store
            datad[header] = convert(data)  # call our all powerful convert function
    return datad


# a list of stock tickers to download and parse
tickers = 'INTC', 'MSFT', 'YHOO', 'GOOG', 'GE', 'WMT', 'CROX'

# we'll store the results in a dictionary of dictionaries.  tickerd is
# keyed off the ticker and points to a data dictionary returned by parse_fname
tickerd = dict()
for ticker, datafile in grab_data(tickers):
    tickerd[ticker] = parse_htmlfile(datafile)
    
# now let's pretty print the data for one ticker
ticker = 'INTC'
maxlen = max([len(header) for header in tickerd[ticker]])
for header, data in tickerd['INTC'].items():
    print '%s: %s'%(header.ljust(maxlen), data)
