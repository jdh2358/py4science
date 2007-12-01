import pylab, numpy
from matplotlib.toolkits.basemap import Basemap
# create figure.
fig = pylab.figure()
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
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
m.drawcountries()
m.drawstates()
# label meridians where they intersect the left, right and bottom
# of the plot frame.
m.drawmeridians(numpy.arange(-180,181,20),labels=[1,1,0,1])
# label parallels where they intersect the  left, right and top
# of the plot frame.
m.drawparallels(numpy.arange(-80,81,20),labels=[1,1,1,0])
pylab.title('labelled meridians and parallels',y=1.075)
pylab.savefig('basemap4.eps')
pylab.savefig('basemap4.png')
