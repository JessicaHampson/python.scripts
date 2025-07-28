from netCDF4 import Dataset, num2date
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import os
import imageio
from PIL import Image
import nclcmaps
# Load the NetCDF file
input_dir = '/archive/Jaeyeon.Lee/Jessica'
file_name = 'TP.1993.nc'
slp_dir = '/archive/Jaeyeon.Lee/Jessica/W2_proj/ERA5/SLP/6hourly'
slp_file = 'slp.T63.o1.1993.nc'
slp_path = os.path.join(slp_dir, slp_file)
filepath = os.path.join(input_dir, file_name)
output_dir = '/home/Jessica.Hampson'
ds = xr.open_dataset(filepath)
precip = ds['tp']
precip_cm = precip *1000

# Select time window: Mar 12 to Mar 14, 1993
precip_subset = precip_cm.sel(
    time=slice('1993-03-12T18:00:00', '1993-03-14T18:00:00'),
    lon=slice(275, 305),
    lat=slice(50, 25)
)
# Create finer coordinate grid (every 0.25 degrees)
new_lat = np.arange(precip_subset.lat.min(), precip_subset.lat.max(), 0.25)
new_lon = np.arange(precip_subset.lon.min(), precip_subset.lon.max(), 0.25)
# Create folder for frames
os.makedirs(output_dir, exist_ok=True)
os.makedirs("frames", exist_ok=True)
filenames = []
increments = precip_subset.diff(dim='time')
cumulative_precip = increments.cumsum(dim='time')
cumulative_interp = cumulative_precip.interp(lat=new_lat, lon=new_lon, method='linear')
vmin = 0
vmax = 13
levels = np.linspace(vmin, vmax,14)
plon, plat = precip_subset['lon'].values, precip_subset['lat'].values
for i in range(1, len(cumulative_interp.time)):
    t_now = cumulative_interp.time[i]
    accumulat fig = plt.figure(figsize=(10, 6),facecolor='white')
    ax = plt.axes(projection=ccrs.PlateCarree(),facecolor='white')
    filled_var=ax.contourf(new_lon,new_lat,accumulation.values,levels=levels,cmap=nclcmaps.cmap('precip2_17lev'),transform=ccrs.PlateCarree(),extend='both')

    plt.title(str(t_now.values))

    cbar=plt.colorbar(filled_var)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label('Total Precipitation (mm)', fontsize=16)

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.set_extent([275, 305, 25, 50], crs=ccrs.PlateCarree())
    # Save frame
    frame_path = os.path.join(output_dir, f'frame_{i:03}.png')
    plt.savefig(frame_path, dpi=100, bbox_inches='tight')
    filenames.append(frame_path)
    plt.close()
# Create GIF
gif_path = os.path.join(output_dir, 'Total_precip5.gif')
frames = [Image.open(f) for f in filenames]

frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],
    duration=1000,
    loop=0
)

print(f"GIF saved to {gif_path}")

    
