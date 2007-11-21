import pylab, numpy
from matplotlib.toolkits.basemap import Basemap

# create figure.
# background color will be used for 'wet' areas.
fig = pylab.figure()
fig.add_axes([0.1,0.1,0.8,0.8],axisbg='aqua')
# create map by specifying lat/lon values at corners.
resolution = 'l'
projection = 'lcc'
lat_0 = 60
lon_0 = -50
llcrnrlat, llcrnrlon = 8, -92
urcrnrlat, urcrnrlon  = 39, 63
m = Basemap(lat_0=lat_0,lon_0=lon_0,\
            llcrnrlat=llcrnrlat,llcrnrlon=llcrnrlon,\
            urcrnrlat=urcrnrlat,urcrnrlon=urcrnrlon,\
            resolution=resolution,projection=projection)
# draw coastlines. Make liness a little thinner than default.
m.drawcoastlines(linewidth=0.5)
# fill continents.
m.fillcontinents(color='coral')
# draw states and countries.
m.drawcountries()
m.drawstates()
pylab.title('map region specified using corner lat/lon values')
pylab.savefig('basemap1.eps')
pylab.savefig('basemap1.png')
