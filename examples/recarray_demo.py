"""
parse and load ge.csv into a record array
"""
import time, datetime, csv
import dateutil.parser
import numpy

if 0:
    # create a csv reader to parse the file
    fh = file('data/ge.csv')
    reader = csv.reader(fh)
    header = reader.next()

    # iterate over the remaining rows and convert the data to date
    # objects, ints, or floats as approriate
    rows = []
    for date, open, high, low, close, volume, adjclose in reader:
        date = dateutil.parser.parse(date).date()
        volume = int(volume)
        open, high, low, close, adjclose = map(float, (
            open, high, low, close, adjclose))
        rows.append((date, open, high, low, close, volume, adjclose))

    fh.close()

    # this is how you can use the function matplotlib.mlab.load to do the same
    #rows = load('data/ge.csv', skiprows=1, converters={0:datestr2num}, delimiter=',')

    r = numpy.rec.fromrecords(rows, names='date,open,high,low,close,volume,adjclose')

# compute the average approximate dollars traded over the last 10 days
# hint: closing price * volume trades approx equals dollars trades
recent = r[-10:]
dollars = numpy.mean(recent.close * recent.volume)
print '$%1.2fM'%(dollars/1e6)

# plot the adjusted closing price vs time since 2003 - hint, you must
# use date2num to convert the date to a float for mpl.  Make two axes,
# one for price and one for volume.  Use a bar chart for volume
import matplotlib
matplotlib.rcParams['usetex'] = False
from matplotlib.dates import date2num
import pylab
mask = r.date>datetime.date(2003,1,1)
date = date2num(r.date[mask])
price = r.adjclose[mask]
volume = r.volume[mask]

fig = pylab.figure()
fig.subplots_adjust(hspace=0)
ax1 = fig.add_subplot(211)
ax1.plot(date, price, '-');
ax1.xaxis_date()
ax1.grid()
for label in ax1.get_xticklabels():
    label.set_visible(False)

ax2 = fig.add_subplot(212, sharex=ax1)
ax2.bar(date, volume);
ax2.xaxis_date()
ax2.grid()
for label in ax2.get_xticklabels():
    label.set_rotation(30)
    label.set_horizontalalignment('right')


pylab.show()
