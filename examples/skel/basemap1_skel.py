import pylab, numpy
from matplotlib.toolkits.basemap import Basemap

# create figure.
# background color will be used for 'wet' areas.
fig = pylab.figure()
fig.add_axes([0.1,0.1,0.8,0.8],axisbg='aqua')
# create map by specifying lat/lon values at corners.
projection = 'lcc' # map projection 
resolution = XX # resolution of boundaries ('c','l','i',or 'h')
lon_0=XX # longitude of origin of map projection domain.
lat_0=XX # standard parallel/latitude of origin of map projection domain.
llcrnrlat, llcrnrlon = XX, XX # lat/lon of lower left corner of map
urcrnrlat, urcrnrlon  = XX, XX # lat/lon of upper right corner of map
m = Basemap(lon_0=lon_0,lat_0=lat_0,\
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
pylab.show()
