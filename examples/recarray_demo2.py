"""
parse and load ge.csv into a record array
"""
import time, datetime, csv
import dateutil.parser
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import numpy as np

# this is how you can use the function np.loadtxt to do the same
# JDH TODO: this isn't working in mlab.load or np.loadtxt.  Fix
#rows = np.loadtxt('data/ge.csv', skiprows=1, converters={0:mdates.date2num}, delimiter=',')
rows = mlab.load('data/ge.csv', skiprows=1, converters={0:mdates.date2num}, delimiter=',')
r = np.rec.fromrecords(rows, names='date,open,high,low,close,volume,adjclose')

# compute the average approximate dollars traded over the last 10 days
# hint: closing price * volume trades approx equals dollars trades
recent = r[-10:]
dollars = (recent.close * recent.volume).mean()
print '$%1.2fM'%(dollars/1e6)

# plot the adjusted closing price vs time since 2003 - hint, you must
# use date2num to convert the date to a float for mpl.  Make two axes,
# one for price and one for volume.  Use a bar chart for volume

import matplotlib.pyplot as plt
dates = mdates.num2date(r.date) # convert these to native datetime.date objects
mask = dates > datetime.date(2003,1,1)
price = r.adjclose[mask]
volume = r.volume[mask]

fig = plt.figure()
fig.subplots_adjust(hspace=0)
ax1 = fig.add_subplot(211)
ax1.plot(dates, price, '-');

ax1.grid()
for label in ax1.get_xticklabels():
    label.set_visible(False)

ax2 = fig.add_subplot(212, sharex=ax1)
ax2.bar(dates, volume);

ax2.grid()
for label in ax2.get_xticklabels():
    label.set_rotation(30)
    label.set_horizontalalignment('right')

fig.autofmt_xdate()
plt.show()
