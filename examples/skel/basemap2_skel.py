import pylab, numpy
from matplotlib.toolkits.basemap import Basemap, supported_projections
# create map by specifying width and height in km.
projection = XX # map projection  ('lcc','stere','laea','aea' etc)
                # 'print supported_projections' gives a list
resolution = XX # resolution of boundaries ('c','l','i',or 'h')
lon_0= XX # longitude of origin of map projection domain (degrees).
lat_0= XX # standard parallel/latitude of origin of map projection domain.
width = XX # width of map projecton domain in km.
height = XX # height of map projection domain in km.
m = Basemap(lon_0=lon_0,lat_0=lat_0,\
            width=width,height=height,\
            resolution=resolution,projection=projection)
m.drawcoastlines(linewidth=0.5)
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
m.drawcountries()
m.drawstates()
pylab.title('map region specified using width and height')
pylab.show()
