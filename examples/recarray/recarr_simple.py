"""Utility module to load measurements into Numpy record arrays.

Loading measurement files with the format:

#Station  Lat    Long   Elev 
BIRA	26.4840	87.2670	0.0120
BUNG	27.8771	85.8909	1.1910
etc...
"""

import numpy as np
import pylab as plt

# Simple example of usage

# Data descriptor to make a proper array.
dt = [('station','S4'),('lat',np.float32),('lon',np.float32),
      ('elev',np.float32)]
# This is an alternate and fully equivalent form:
dt = dict(names = ('station','lat','lon','elev'),
          formats = ('S4',np.float32,np.float32,np.float32) )

# For more on dtypes, see:
# http://mentat.za.net/numpy/refguide/arrays.recarray.xhtml
import math

def tlog(s):
    return np.float32(math.log(float(s)))

tab = np.loadtxt('HIMNTstations2.txt',dt,
                 converters={1:tlog})

print 'Stations:',tab['station']
print 'Elevations:',tab['elev']
print 'First station:',tab[0]
print 'Mean latitude:',tab['lat'].mean()

plt.figure()
plt.scatter(tab['lat'],tab['lon'],30*tab['elev'],
            c=tab['elev'],
            cmap=plt.cm.bone,
            )
plt.show()
