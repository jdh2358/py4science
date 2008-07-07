"""Simple data access and manipulation demo, using Yahoo Finance data."""

# <demo> stop

# Needed libraries
import urllib
import matplotlib.mlab as mlab  # contains csv2rec
import pylab as p

# <demo> stop

# Choose a stock, make the URL for it and download it to a local file
ticker = 'CROX'  # Boulder-based company Crocs

url = 'http://ichart.finance.yahoo.com/table.csv?' +\
      's=%s&d=9&e=20&f=2007&g=d&a=0&b=29&c=1993&ignore=.csv'%ticker

fname = '%s.csv'% ticker
urllib.urlretrieve(url, fname)

# <demo> stop

# Now, make a Record Array out of this dataset:
r = mlab.csv2rec(fname)

# note that the CSV file is sorted most recent date first, so you will probably
# want to sort the record array so most recent date is last
r.sort()
# A quick look at the data structure:
print 'dtype:',r.dtype
print 'shape:',r.shape

# <demo> stop

p.plot(r.date,r.adj_close)
p.show()

# <demo> stop
# Now, make a slightly modified version of the file with cleaner formatting.
# We'll use this later...
#
