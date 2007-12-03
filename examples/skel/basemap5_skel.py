from matplotlib.toolkits.basemap import Basemap, NetCDFFile, cm
import pylab, numpy
# read in netCDF sea-surface temperature data
# can be a local file, a URL for a remote opendap dataset,
# or (if PyNIO is installed) a GRIB or HDF file.
# See http://nomads.ncdc.noaa.gov/ for some NOAA OPenDAP datasets.
ncfile = NetCDFFile('data/sst.nc')
# uncommenting the next line will produce a very similar plot,
# but will read the data over the web instead of from a local file. 
#ncfile = NetCDFFile('http://nomads.ncdc.noaa.gov:8085/thredds/dodsC/oisst/2007/AVHRR/sst4-navy-eot.20071201.nc')
sst = ncfile.variables['sst'][:]
lats = ncfile.variables['lat'][:]
lons = ncfile.variables['lon'][:]
# Basemap comes with extra colormaps from Generic Mapping Tools
# (imported as cm, pylab colormaps in pylab.cm)
cmap = XX
# create Basemap instance for mollweide projection.
projection = XX # try moll, robin, sinu or ortho.
# coastlines not used, so resolution set to None to skip
# continent processing (this speeds things up a bit)
m = Basemap(projection=projection,lon_0=lons.mean(),lat_0=0,resolution=None)
# compute map projection coordinates of grid.
x, y = m(*numpy.meshgrid(lons, lats))
# plot with pcolor
im = m.pcolormesh(x,y,sst,shading='flat',cmap=cmap)
# or try 100 filled contours.
#CS = m.contourf(x,y,sst,100,cmap=cmap)
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
