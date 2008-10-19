from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# create map by specifying width and height in km.
resolution = 'l'; projection = 'lcc'
lon_0 = -50; lat_0 = 60
width = 12000000; height = 0.75*width
m = Basemap(lon_0=lon_0,lat_0=lat_0,\
            width=width,height=height,\
            resolution=resolution,projection=projection)
m.drawcoastlines(linewidth=0.5)
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
m.drawcountries()
m.drawstates()
plt.title('map region specified using width and height')
plt.show()
