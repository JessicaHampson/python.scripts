import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import seaborn as sns
from trackfunc2 import trackdist
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import nclcmaps
era5_dir_tracks = '/archive/Jaeyeon.Lee/Jessica/W1_proj'
dir_filtered = '/archive/Jessica.Hampson'
dir_tracks = '/archive/Jaeyeon.Lee/Jessica'
track_id_var = "xslb_ti00"
LON_RANGE = [245,355]
LAT_RANGE = [25,75]
GRID_DEG =1.5
START_YEAR, END_YEAR = 1991, 2020

NYEARS = END_YEAR - START_YEAR + 1
NMONTH = 12
tot_freq = []
for i in range(1, 6):
    ens = f'ens0{i}' 
    track_file = os.path.join(dir_tracks, f'trackread63_{ens}_SLP_19912020_SPEAR-LO_NH_dist.npz')
    filtered_file = os.path.join(dir_filtered, f'bomb_cyc_NovtoMar_SPEAR-LOW_{ens}.npz')
    # making sure files exist
    if os.path.exists(track_file) and os.path.exists(filtered_file):
        track_data = np.load(track_file)
        filtered_data = np.load(filtered_file)

        # Access track IDs
        if track_id_var in filtered_data:
            track_ids = filtered_data[track_id_var]
            print(f"{ens}: Loaded {len(np.unique(track_ids))} bomb cyclone tracks.")
        else:
            print(f"{ens}: Variable '{track_id_var}' not found in filtered file.")
    else:
        print(f"{ens}: One or both files not found.")

    # LOAD DATA
    with np.load(filtered_file) as f:
       track_subset = f[track_id_var]
    f = np.load(track_file)
    for v in f.files:
        exec(v+'=f[v]')

    freq_counts = trackdist(track_subset, 555,
                            LON_RANGE, LAT_RANGE,
                            track_file, GRID_DEG,
                            var="freq")
    tot_freq.append(freq_counts)


#  COMBINE & COMPUTE FREQ
tot_freq = np.array(tot_freq)
freq_counts1 = np.mean(tot_freq[:,:,:],axis=0)
M_freq = freq_counts1 / NYEARS # mean monthly frequency
#plot 
# build grid
lon_grid = np.arange(LON_RANGE[0], LON_RANGE[1] + GRID_DEG, GRID_DEG)
lat_grid = np.arange(LAT_RANGE[0], LAT_RANGE[1] + GRID_DEG, GRID_DEG)
# add cyclic point for seamless map
freq_cyc, lon_cyc = add_cyclic_point(M_freq, coord=lon_grid)
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.Mercator(central_longitude=265))
cf = ax.contourf(lon_cyc, lat_grid, freq_cyc,
                 levels=np.arange(1,9,0.25),cmap=nclcmaps.cmap('MPL_jet'),
                 extend="max", transform=ccrs.PlateCarree())
ax.coastlines(resolution="110m")
ax.add_feature(cfeature.BORDERS.with_scale("110m"), linewidth=0.5)
ax.set_xticks(np.arange(LON_RANGE[0],LON_RANGE[1]+1,25), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(LAT_RANGE[0], LAT_RANGE[1] + 1, 10), crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.tick_params(labelsize=16)
ax.set_title('SPEAR-LO',fontsize=20)
cbar = fig.colorbar(cf, orientation="vertical", pad=0.01, fraction=0.05,
                    label="# bomb cyclones / year")
cbar.ax.tick_params(labelsize=14)
cbar.set_label(label='# Bomb Cyclones / Year', fontsize=17)

plt.tight_layout()
plt.show()
