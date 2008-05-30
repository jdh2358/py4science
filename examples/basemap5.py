from mpl_toolkits.basemap import Basemap, NetCDFFile
import matplotlib.pyplot as plt
import numpy as np
# read in netCDF sea-surface temperature data
# can be a local file, a URL for a remote opendap dataset,
# or (if PyNIO is installed) a GRIB or HDF file.
ncfile = NetCDFFile('data/sst.nc')
sst = ncfile.variables['sst'][:]
lats = ncfile.variables['lat'][:]
lons = ncfile.variables['lon'][:]
# create Basemap instance for mollweide projection.
# coastlines not used, so resolution set to None to skip
# continent processing (this speeds things up a bit)
m = Basemap(projection='moll',lon_0=0,lat_0=0,resolution=None)
# compute map projection coordinates of grid.
x, y = m(*np.meshgrid(lons, lats))
# plot with pcolor
im = m.pcolormesh(x,y,sst,shading='flat',cmap=plt.cm.gist_ncar)
# draw parallels and meridians, but don't bother labelling them.
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,420.,60.))
# draw line around map projection limb.
# color map region background black (missing values will be this color)
m.drawmapboundary(fill_color='k')
# draw horizontal colorbar.
plt.colorbar(orientation='horizontal')
plt.show()
