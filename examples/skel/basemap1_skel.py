import pylab, numpy
from matplotlib.toolkits.basemap import Basemap

# create figure.
fig = pylab.figure()
# create map by specifying lat/lon values at corners.
projection = 'lcc' # map projection 
resolution = XX # resolution of boundaries ('c','l','i',or 'h')
lon_0=XX # longitude of origin of map projection domain (degrees).
lat_0=XX # standard parallel/latitude of origin of map projection domain.
llcrnrlat, llcrnrlon = XX, XX # lat/lon of lower left corner of map (degrees)
urcrnrlat, urcrnrlon  = XX, XX # lat/lon of upper right corner of map
m = Basemap(lon_0=lon_0,lat_0=lat_0,\
            llcrnrlat=llcrnrlat,llcrnrlon=llcrnrlon,\
            urcrnrlat=urcrnrlat,urcrnrlon=urcrnrlon,\
            resolution=resolution,projection=projection)
# draw coastlines. Make liness a little thinner than default.
m.drawcoastlines(linewidth=0.5)
# background fill color will show ocean areas.
m.drawmapboundary(fill_color='aqua')
# fill continents, lakes within continents.
m.fillcontinents(color='coral',lake_color='aqua')
# draw states and countries.
m.drawcountries()
m.drawstates()
pylab.title('map region specified using corner lat/lon values')
pylab.show()
