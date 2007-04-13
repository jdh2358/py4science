"""
parse and load ge.csv into a record array
"""
import time, datetime, csv
import dateutil.parser
import numpy

XXX = None
# create a csv reader to parse the file
fh = file('data/ge.csv')
reader = csv.reader(fh)
header = reader.next()

# iterate over the remaining rows and convert the data to date
# objects, ints, or floats as approriate
rows = []
for date, open, high, low, close, volume, adjclose in reader:
    XXX # conver the strings here
    rows.append((date, open, high, low, close, volume, adjclose))

fh.close()

# this is how you can use the function matplotlib.mlab.load to do the same
#rows = load('data/ge.csv', skiprows=1, converters={0:datestr2num}, delimiter=',')

r = numpy.rec.fromrecords(rows, names='date,open,high,low,close,volume,adjclose')

# compute the average approximate dollars traded over the last 10 days
# hint: closing price * volume trades approx equals dollars trades
XXX

# plot the adjusted closing price vs time since 2003 - hint, you must
# use date2num to convert the date to a float for mpl.  Make two axes,
# one for price and one for volume.  Use a bar chart for volume
import matplotlib
matplotlib.rcParams['usetex'] = False

XXX
