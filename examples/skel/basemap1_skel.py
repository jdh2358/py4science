from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# create map by specifying lat/lon values at corners.
resolution = 'l'; projection = 'lcc'
lat_0 = 60; lon_0 = -50
llcrnrlat, llcrnrlon = 8, -92
urcrnrlat, urcrnrlon  = 39, 63
m = Basemap(lat_0=lat_0,lon_0=lon_0,\
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
plt.title('map region specified using corner lat/lon values')
plt.show()
