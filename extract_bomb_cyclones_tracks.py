import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
# paths
dir_tracks = '/archive/Jaeyeon.Lee/Jessica/W1_proj'
dir_filtered = '/archive/Jessica.Hampson'
filtered_file = os.path.join(dir_filtered, 'output_NovtoMar_filtered_cyclones_final.npz')
track_file    = os.path.join(dir_tracks, 'trackread63_SLP_19912020_ERA5_dist.npz')
# load in events
if not os.path.exists(filtered_file):
    raise FileNotFoundError(f"Filtered data file not found: {filtered_file}")

filtered = np.load(filtered_file)
if 'ext_ti00' not in filtered or 'ext_stlon00' not in filtered or 'ext_stlat00' not in filtered:
    raise KeyError("'your_filtered_data.npz' must contain 'ext_ti00', 'ext_stlon00', 'ext_stlat00'")
# load orginial track data 
if not os.path.exists(track_file):
    raise FileNotFoundError(f"Track data file not found: {track_file}")

tracks = np.load(track_file)
if 'eventarray' not in tracks or 'lonc' not in tracks or 'latc' not in tracks:
    raise KeyError("'original_track_output.npz' must contain 'eventarray', 'lonc', 'latc'")

eventarray = tracks['eventarray']
lonc = tracks['lonc']
latc = tracks['latc']
hr = tracks['longhr']
day = tracks['longday']
mon = tracks['longmon']
yr = tracks['longyear']
time = tracks['timec']
int = tracks['Revc']
# extract bomb cyclones 
bomb_indicies = []
bomb_stlons = []
bomb_stlats = []
bomb_lons = []
bomb_lats = []
bomb_lifetime = []
bomb_int = []

event_ids = (filtered['ext_ti00'])     # int array of event IDs to plot
event_lifetime = (filtered['ext_num00'])
start_lons = (filtered['ext_stlon00'])  # float array: start longitude per event
start_lats = (filtered['ext_stlat00'])  # float array: start latitude per event
track_int = (filtered['ext_revc00'])
all_lons = (filtered['ext_lon00'])
all_lats = (filtered['ext_lat00'])
for i in range(len(event_ids)):
    index = np.where(eventarray == event_ids[i])[0]
    cyc_int = int[index]
    cyc_lat = latc[index]

    dp = []
    for j in range(len(cyc_int) - 2):
        rate = cyc_int[j+2] - cyc_int[j]
        lat_mid= 0.5 * (cyc_lat[j+2] + cyc_lat[j])
        threshold = 12.0 * np.sin(np.deg2rad(lat_mid))/np.sin(np.deg2rad(60))
          if rate >= threshold:
            bomb_indicies.append(event_ids[i])
            bomb_stlons.append(lonc[index[0]])
            bomb_stlats.append(latc[index[0]])
            bomb_lifetime.append(eventarray[index])
            bomb_int.append(int[index])
            break
# Plotting 
LON_MIN, LON_MAX = -125.0, -30.0
LAT_MIN, LAT_MAX =   24.0,  55.0

fig = plt.figure(figsize=(10,8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_aspect(1.1)
ax.set_title("ERA5: Bomb Cyclone Tracks", fontsize=23)
ax.coastlines(resolution='50m', linewidth=1)
ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
#  loop over filtered events 
for evt_id, stlon, stlat in tqdm(zip(bomb_indicies, bomb_stlons, bomb_stlats),
                                  total=len(bomb_indicies),
                                  desc='Processing events'):
    idx = np.where(eventarray == evt_id)[0]
    if idx.size == 0:
        continue

    track_lons = fix_lons[idx]
    track_lats = latc[idx]
    track_stlons = fix_lons[idx]
    track_stlats = latc[idx]
    track_event = eventarray[idx]
    track_hrs = hr[idx]
    track_days = day[idx]
    track_mon = mon[idx]
    track_yr = yr[idx]
    track_time = time[idx]
    track_intensity = int[idx]
    ax.plot(track_lons, track_lats,
            color='black', alpha=0.5, linewidth=0.7,
            transform=ccrs.PlateCarree())

   ax.scatter(track_lons, track_lats,
           facecolor='white', edgecolor='black',
           linewidth=1.5, alpha=1, s=20,
           transform=ccrs.PlateCarree(), zorder=3)
# box around NA region
box_min_lon, box_max_lon, box_min_lat, box_max_lat = -85, -60, 25, 47

box_lon = [box_min_lon, box_max_lon, box_max_lon, box_min_lon, box_min_lon]

box_lat =[box_min_lat, box_min_lat, box_max_lat, box_max_lat, box_min_lat]

ax.plot(box_lon, box_lat,linewidth = 2, color ='red',
transform=ccrs.PlateCarree())
ax.set_extent([LON_MIN, LON_MAX, LAT_MIN, LAT_MAX], ccrs.PlateCarree())
plt.show()
output_dir = '/archive/Jessica.Hampson'
os.makedirs(output_dir, exist_ok=True)
outfile = os.path.join(output_dir, f'output_NovtoMar_bomb_cyclone_tracks.npz')
np.savez(
    outfile,
    xbcyc_lon00=np.array(track_lons),
    xbcyc_lat00=np.array(track_lats),
    xbcyc_ti00=np.array(bomb_indicies),
    xbcyc_num00=np.array(event_lifetime),#before was track_event
    xbcyc_hr00=np.array(track_hrs),
    xbcyc_day00=np.array(track_days),
    xbcyc_mon00=np.array(track_mon),
    xbcyc_yr00=np.array(track_yr),
    xbcyc_time00=np.array(track_time),
    xbcyc_int00=np.array(track_int),
    #xbcyc_stlon00=np.array(bomb_stlons),
    #xbcyc_stlat00=np.array(bomb_stlats),
#    bcyc_stmon00=np.array(filtered['all_stmon00'])#[:1],
#    bcyc_styr00=np.array(filtered['all_styr00'])#[:1],
)
print(f"Filtered data saved to:{outfile}")

