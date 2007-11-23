from matplotlib.toolkits.basemap import Basemap, NetCDFFile
import pylab, numpy
from numpy import ma

# read in netCDF sea-surface temperature data
ncfile = NetCDFFile('data/sst.nc')
sstv = ncfile.variables['analysed_sst']
sst = ma.masked_values(numpy.squeeze(sstv[:]), sstv._FillValue)
sst = sstv.scale_factor*sst + sstv.add_offset
lats = ncfile.variables['lat'][:]
lons = ncfile.variables['lon'][:]
print sst.shape, sst.min(), sst.max()

# make sure middle of map region is middle of data grid.
lon_0 = lons.mean()
lat_0 = lats.mean()
# set colormap
cmap = pylab.cm.gist_ncar
# set so masked values in an image will be black
# (i.e. continents will be painted this color)
cmap.set_bad('k')
# create Basemap instance for mollweide projection.
# coastlines not used, so resolution set to None to skip
# continent processing (this speeds things up a bit)
m = Basemap(projection='moll',lon_0=lon_0,lat_0=lat_0,resolution=None)
# compute map projection coordinates of grid.
x, y = m(*numpy.meshgrid(lons, lats))
# plot with pcolor
im = m.pcolormesh(x,y,sst,shading='flat',cmap=cmap)
# draw parallels and meridians, but don't bother labelling them.
m.drawparallels(numpy.arange(-90.,120.,30.))
m.drawmeridians(numpy.arange(0.,420.,60.))
# draw line around map projection limb.
m.drawmapboundary()
# draw horizontal colorbar.
pylab.colorbar(orientation='horizontal')
pylab.savefig('basemap5.pdf') # eps files are too huge when pcolor used.
pylab.savefig('basemap5.png')
