import pylab, numpy
from matplotlib.toolkits.basemap import Basemap

# create figure.
fig = pylab.figure()
# create map by specifying width and height in km.
resolution = 'l'
projection = 'lcc'
lon_0 = -50
lat_0 = 60
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
pylab.title('map region specified using width and height')
pylab.savefig('basemap2.eps')
pylab.savefig('basemap2.png')
