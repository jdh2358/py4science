from matplotlib.toolkits.basemap import Basemap, NetCDFFile, cm
import pylab, numpy

# read in netCDF sea-surface temperature data
# can be a local file, a URL for a remote opendap dataset,
# or (if PyNIO is installed) a GRIB or HDF file.
ncfile = NetCDFFile('data/sst.nc')
sst = ncfile.variables['analysed_sst'][:]
lats = ncfile.variables['lat'][:]
lons = ncfile.variables['lon'][:]

print sst.shape, sst.min(), sst.max()

# Basemap comes with extra colormaps from Generic Mapping Tools
# (imported as cm, pylab colormaps in pylab.cm)
cmap = XX
# create Basemap instance for mollweide projection.
projection = XX # try moll, robin, sinu or ortho.
# coastlines not used, so resolution set to None to skip
# continent processing (this speeds things up a bit)
m = Basemap(projection=projection,lon_0=0,lat_0=0,resolution=None)
# compute map projection coordinates of grid.
x, y = m(*numpy.meshgrid(lons, lats))
# plot with pcolor
im = m.pcolormesh(x,y,sst,shading='flat',cmap=cmap)
# draw parallels and meridians, but don't bother labelling them.
m.drawparallels(numpy.arange(-90.,120.,30.))
m.drawmeridians(numpy.arange(0.,420.,60.))
# draw line around map projection limb.
# color map region background (missing values will be this color)
color = XX
m.drawmapboundary(fill_color=color)
# draw horizontal colorbar.
pylab.colorbar(orientation='horizontal')
pylab.show()
