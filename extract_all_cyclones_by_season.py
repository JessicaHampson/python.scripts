import numpy as np
import os
start_year = 1991
end_year = 2020
model_name = 'ERA5'
ensemble_number = 1
target_months = np.array([11, 12, 1, 2, 3])
input_dir = '/arch5/j4l/Jessica/W1_proj'
output_dir = '/archive/Jessica.Hampson'
file_path = os.path.join(input_dir, f'trackread63_SLP_19912020_{model_name}_dist.npz')
print(f"Loading data from: {file_path}")
f = np.load(file_path)
data = {v: f[v] for v in f.files} 
# Extract Coords
lats = f['latc'][:]
lons = f['lonc'][:]
lat_bnds, lon_bnds = [24.5, 45.0], [278.5, 293.5]
region_inds = np.where((lats > lat_bnds[0]) & (lats < lat_bnds[1]) & (lons > lon_bnds[0]) & (lons < lon_bnds[1]))[0]
event_filter, year_filter, month_filter, day_filter, hour_filter, grc_filter, time_filter, rev_filter = f['eventarray'][region_inds], f['longyear'][region_inds], f['longmon'][region_inds], f['longday'][region_inds], f['longhr'][region_inds], f['grc'][region_inds], f['timec'][region_inds], f['Revc'][region_inds]
# Output containers 
ext_lon00 = []
ext_lat00 = []
ext_ti00 = []
ext_num00 = []
ext_hr00 = []
ext_day00 = []
ext_time00 = []
ext_mon00 = []
ext_yr00 = []
ext_stmon00 = []
ext_styr00 = []
ext_stlon00 = []
ext_stlat00 = []
ext_revc00=[]
# Extract 
selected = np.isin(data['longmon'],target_months)
target_event_ids = np.unique(data['eventarray'][selected])
index = np.isin(month_filter, target_months)
selected_months  = np.unique(month_filter[index])
selected_events = np.unique(event_filter[index])
# Reconsturction loop
from tqdm import tqdm
for i in tqdm(range(len(selected_events)), desc="Constructing filtered track data"):
    tid = selected_events[i]
    whtr = np.where(data['eventarray'] == tid)[0]

    ext_lon00.extend(data['lonc'][whtr])
    ext_lat00.extend(data['latc'][whtr])
    ext_hr00.extend(data['longhr'][whtr])
    ext_day00.extend(data['longday'][whtr])
    ext_mon00.extend(data['longmon'][whtr])
    ext_yr00.extend(data['longyear'][whtr])
    ext_num00.extend(data['eventarray'][whtr])
    ext_time00.extend(data['timec'][whtr])
    ext_revc00.extend(data['Revc'][whtr])

    ext_stlon00.append(data['lonc'][whtr[0]])
    ext_stlat00.append(data['latc'][whtr[0]])
    ext_ti00.append(data['eventarray'][whtr[0]])
    ext_stmon00.append(data['longmon'][whtr[0]])
    ext_styr00.append(data['longyear'][whtr[0]])
# Save 
os.makedirs(output_dir, exist_ok=True)
outfile = os.path.join(output_dir, f'output_NovtoMar_filtered_cyclones_final.npz')
np.savez(
    outfile,
    ext_lon00=np.array(ext_lon00),
    ext_lat00=np.array(ext_lat00),
    ext_ti00=np.array(ext_ti00),
    ext_num00=np.array(ext_num00),
    ext_hr00=np.array(ext_hr00),
    ext_day00=np.array(ext_day00),
    ext_mon00=np.array(ext_mon00),
    ext_yr00=np.array(ext_yr00),
    ext_time00=np.array(ext_time00),
    ext_stlon00=np.array(ext_stlon00),
    ext_stlat00=np.array(ext_stlat00),
    ext_stmon00=np.array(ext_stmon00),
    ext_styr00=np.array(ext_styr00),
    ext_revc00=np.array(ext_revc00),
)
print(f"Filtered data saved to: {outfile}")
