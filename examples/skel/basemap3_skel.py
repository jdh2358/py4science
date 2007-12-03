import pylab, numpy
from matplotlib.toolkits.basemap import Basemap
# create map by specifying width and height in km.
resolution = 'l'; projection='lcc'
lon_0 = -50; lat_0 = 60.
width = 12000000; height = 0.75*width
m = Basemap(lon_0=lon_0,lat_0=lat_0,width=width,height=height,\
            resolution=resolution,projection=projection)
# lat/lon and name of location 1.
lat1 = XX; lon1 = XX; name = XX
# ditto for location 2.
lat2 = XX; lon2 = XX; name2 = XX
# convert these points to map projection coordinates
# (using __call__ method of Basemap instance)
x1, y1 = m(lon1, lat1)
x2, y2 = m(lon2, lat2)
# plot black dots at the two points.
# make sure dots are drawn on top of other plot elements (zorder=10)
m.scatter([x1,x2],[y1,y2],25,color='k',marker='o',zorder=10)
# connect the dots along a great circle.
m.drawgreatcircle(lon1,lat1,lon2,lat2,linewidth=2,color='k')
# put the names of the cities to the left of each dot, offset
# by a little. Use a bold font.
pylab.text(x1-100000,y1+100000,name1,fontsize=12,\
           color='k',horizontalalignment='right',fontweight='bold')
pylab.text(x2-100000,y2+100000,name2,fontsize=12,\
           color='k',horizontalalignment='right',fontweight='bold')
m.drawcoastlines(linewidth=0.5)
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
m.drawcountries()
m.drawstates()
pylab.title(name1+' to '+name2+' Great Circle')
pylab.show()
