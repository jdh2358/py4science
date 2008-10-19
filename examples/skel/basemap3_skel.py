from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# create map by specifying width and height in km.
resolution = 'l'; projection = 'lcc'
lon_0 = -50; lat_0 = 60
width = 12000000; height = 0.75*width
m = Basemap(lon_0=lon_0,lat_0=lat_0,width=width,height=height,
            resolution=resolution,projection=projection)
# nylat, nylon are lat/lon of New York
nylat = 40.78
nylon = -73.98
# lonlat, lonlon are lat/lon of London.
lonlat = 51.53
lonlon = 0.08
# convert these points to map projection coordinates
# (using __call__ method of Basemap instance)
ny_x, ny_y = m(nylon, nylat)
lon_x, lon_y = m(lonlon, lonlat)
# plot black dots at the two points.
# make sure dots are drawn on top of other plot elements (zorder=10)
m.scatter([ny_x,lon_x],[ny_y,lon_y],25,color='k',marker='o',zorder=10)
# connect the dots along a great circle.
m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='k')
# put the names of the cities to the left of each dot, offset
# by a little. Use a bold font.
plt.text(ny_x-100000,ny_y+100000,'New York',fontsize=12,\
           color='k',horizontalalignment='right',fontweight='bold')
plt.text(lon_x-100000,lon_y+100000,'London',fontsize=12,\
           color='k',horizontalalignment='right',fontweight='bold')
m.drawcoastlines(linewidth=0.5)
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
m.drawcountries()
m.drawstates()
plt.title('NY to London Great Circle')
plt.show()
