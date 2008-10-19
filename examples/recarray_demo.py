"""
parse and load ge.csv into a record array
"""

import datetime

import numpy as np

import matplotlib
from matplotlib import pyplot as plt

# Disable latex support just in case, so we can rotate text
matplotlib.rcParams['text.usetex'] = False

# Load a data file into a record array using the matplotlib csv2rec utility
r = matplotlib.mlab.csv2rec('data/ge.csv')
r.sort()  #sort by date, the first column

# compute the average approximate dollars traded over the last 10 days
# hint: closing price * volume trades approx equals dollars trades
recent = r[-10:]
dollars = np.mean(recent.close * recent.volume)
print 'Total traded over last 10 days: $%1.2fM'%(dollars/1e6)

# plot the adjusted closing price vs time since 2003.  Make two axes, one for
# price and one for volume.  Use a bar chart for volume

# Record arrays are like 'mini-spreadsheets'
mask = r.date > datetime.date(2003,1,1)
date = r.date[mask]
price = r.adj_close[mask]
volume = r.volume[mask]

# Plotting
fig = plt.figure()
fig.subplots_adjust(hspace=0)
ax1 = fig.add_subplot(211)
ax1.plot(date, price, '-')

ax1.grid()
for label in ax1.get_xticklabels():
    label.set_visible(False)

ax2 = fig.add_subplot(212, sharex=ax1)
ax2.bar(date, volume);

ax2.grid()
for label in ax2.get_xticklabels():
    label.set_rotation(30)
    label.set_horizontalalignment('right')

fig.autofmt_xdate()
plt.show()
