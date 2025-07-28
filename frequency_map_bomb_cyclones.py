import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import nclcmaps
from trackfunc1 import trackdist
dir_tracks = '/archive/Jaeyeon.Lee/Jessica/W1_proj'
TRACK_FILE = os.path.join(dir_tracks, 'trackread63_SLP_19912020_ERA5_dist.npz')
dir_filtered = '/archive/Jessica.Hampson'
FILTERED_TRACK_FILE = os.path.join(dir_filtered, 'output_NovtoMar_bomb_cyclone_tracks.npz')
TRACK_ID  = "xbcyc_ti00"    
LON_RANGE = [245,355]
LAT_RANGE = [25, 75]
GRID_DEG  = 1.5
START_YEAR, END_YEAR = 1991, 2020

NYEARS = END_YEAR - START_YEAR + 1
NMONTH = 12 
# load data 
with np.load(FILTERED_TRACK_FILE) as f:
    track_subset = f[TRACK_ID]
f = np.load(TRACK_FILE)
for v in f.files:
    exec(v+'=f[v]')
#compute frequency
freq_counts = trackdist(track_subset, 555,
                        LON_RANGE, LAT_RANGE,
                        TRACK_FILE, GRID_DEG,
                        var="freq")
freq = freq_counts / NYEARS # mean monthly frequency
# plot 
lon_grid = np.arange(LON_RANGE[0], LON_RANGE[1] + GRID_DEG, GRID_DEG)
lat_grid = np.arange(LAT_RANGE[0], LAT_RANGE[1] + GRID_DEG, GRID_DEG)
freq_cyc, lon_cyc = add_cyclic_point(freq, coord=lon_grid)

fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.Mercator(central_longitude=265))
cf = ax.contourf(lon_cyc, lat_grid, freq_cyc,
                 levels=np.arange(1, 9, 0.25), cmap=nclcmaps.cmap('MPL_jet'),
                 extend="max", transform=ccrs.PlateCarree())
ax.coastlines(resolution="110m")
ax.add_feature(cfeature.BORDERS.with_scale("110m"), linewidth=0.5)
ax.set_xticks(np.arange(LON_RANGE[0],LON_RANGE[1]+1,25), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(LAT_RANGE[0], LAT_RANGE[1] + 1, 10), crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.tick_params(labelsize=16)
ax.set_title('ERA5',fontsize=20)
cbar = fig.colorbar(cf, orientation="vertical", pad=0.01, fraction=0.05,
                    label="# bomb cyclones / year")
cbar.ax.tick_params(labelsize=14)
cbar.set_label(label='# Bomb Cyclones / Year', fontsize=17)

plt.tight_layout()
plt.show()
             
