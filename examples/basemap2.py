import pylab, numpy
from matplotlib.toolkits.basemap import Basemap

# create figure.
# background color will be used for 'wet' areas.
fig = pylab.figure()
fig.add_axes([0.1,0.1,0.8,0.8],axisbg='aqua')
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
# draw coastlines.
m.drawcoastlines(linewidth=0.5)
# fill continents.
m.fillcontinents(color='coral')
# draw states and countries.
m.drawcountries()
m.drawstates()
pylab.title('map region specified using width and height')
pylab.savefig('basemap2.eps')
pylab.savefig('basemap2.png')
