import pylab, numpy
from matplotlib.toolkits.basemap import Basemap
# create figure.
# background color will be used for 'wet' areas.
fig = pylab.figure()
fig.add_axes([0.1,0.1,0.8,0.8],axisbg='aqua')
# create map by specifying width and height in km.
resolution = 'l'
lon_0 = -50
lat_0 = 60
projection = 'lcc'
width = 12000000
height = 0.75*width
m = Basemap(lon_0=lon_0,lat_0=lat_0,\
            width=width,height=height,\
            resolution=resolution,projection=projection)
m.drawcoastlines(linewidth=0.5)
m.fillcontinents(color='coral')
m.drawcountries()
m.drawstates()
# draw and label parallels.
# labels is list of 4 values (default [0,0,0,0]) that control whether
# parallels are labelled where they intersect the left, right, top or
# bottom of the plot. For example labels=[1,0,0,1] will cause parallels
# to be labelled where they intersect the left and bottom of the plot,
# but not the right and top.
labels = XX
parallels = XX # a sequence of latitudes values
m.drawparallels(parallels,labels=labels)
# draw and label meridians.
labels = XX
meridians = XX # a sequence of longitude values
m.drawmeridians(meridians,labels=labels)
pylab.title('labelled meridians and parallels',y=1.075)
pylab.show()
