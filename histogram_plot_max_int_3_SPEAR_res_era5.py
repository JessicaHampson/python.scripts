import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import sys
input_dir = '/archive/Jessica.Hampson'
months = [11, 12, 1, 2, 3]
nmonths = len(months)
ensset = [1, 2, 3, 4, 5]
nens = len(ensset)
mn = ['SPEAR-LOW', 'SPEAR-MED', 'SPEAR-HI']
res_name = ['xslb','xsmb','xshb']
# ERA5
data = os.path.join(input_dir, 'output_NovtoMar_bomb_cyclone_tracks.npz')
f=np.load(data)
for v in f.files:
        exec(v+'=f[v]')
# Preallocate arrays (assumes max 40000 entries per ensemble)
li01 = np.full((5, 40000), -999.0)  # low
mi01 = np.full((5, 40000), -999.0)  # med
hi01 = np.full((5, 40000), -999.0)  # high

for i, md in enumerate(mn):  # model: LOW, MED, HI
    res = res_name[i]  # matching resolution name: xslb, xsmb, xshb
    for j, ens in enumerate(tqdm(ensset, desc=f'{md} processing')):
        ens_str = f'0{ens}'
        file_path = os.path.join(input_dir, f'bomb_cyc_NovtoMar_{md}_ens{ens_str}.npz')

        if not os.path.exists(file_path):
            print(f'File not found: {file_path}')
            continue

        f = np.load(file_path)

        # Check if expected keys exist
        ti_key_name = f'{res}_ti00'
        num_key_name = f'{res}_num00'
        int_key_name = f'{res}_int00'

        if ti_key_name not in f.files or num_key_name not in f.files or int_key_name not in f.files:
            print(f'Keys {ti_key_name} or {num_key_name} or {int_key_name} not found in {file_path}')
            continue

        ti_key = f[ti_key_name]
        num_key = f[num_key_name]
        int_key = f[int_key_name]

         # Compute maximum intensities
        NP_ti = []
        for t in range(len(ti_key)):
            idx = np.where(num_key == ti_key[t])[0]
            num_days = len(idx) / 4  # assuming 4 time steps per day
            bcyc_int = int_key[idx]

            if bcyc_int.size > 0:
                bmax_int = np.max(bcyc_int)
                NP_ti.append(bmax_int)

        NP_ti = np.array(NP_ti)
        nti = len(NP_ti)

        if md == 'SPEAR-LOW':
            li01[j, :nti] = NP_ti
        elif md == 'SPEAR-MED':
            mi01[j, :nti] = NP_ti
        elif md == 'SPEAR-HI':
            hi01[j, :nti] = NP_ti
# plot 
plt.figure(figsize=(16,8))
ax1 = plt.subplot2grid((3,2),(0,0),rowspan=2)
plt.subplots_adjust(hspace=0)
bins = np.linspace(0,75,12)  # set bin interval
xticks = np.arange(5,75,5)  # set x axis ticks
yticks = np.arange(0,120,20)  # set y axis ticks

n1,x1,_ = plt.hist(NP_ti,bins,alpha=0.4,edgecolor='white',color='white')
bin_centers1 = 0.5*(x1[1:]+x1[:-1])

n22 = np.zeros((nens,len(n1)),dtype='f')
n33 = np.zeros((nens,len(n1)),dtype='f')
n44 = np.zeros((nens,len(n1)),dtype='f')

whnan_hi = np.where(hi01 == -999)
hi01[whnan_hi[0],whnan_hi[1]] = np.nan
whnan_mi = np.where(mi01 == -999)
mi01[whnan_mi[0],whnan_mi[1]] = np.nan
whnan_li = np.where(li01 == -999)
li01[whnan_li[0],whnan_li[1]] = np.nan

ag22 = np.zeros((nens),dtype='f')
ag33 = np.zeros((nens),dtype='f')
ag44 = np.zeros((nens),dtype='f')
# calculating histograms of each ensemble
for i in range(nens):
     dum2, x2,_ = plt.hist(hi01[i,:],bins,alpha=0.4,edgecolor='white',color='white')
     n22[i,:] = dum2
     ag22[i] = np.nanmean(hi01[i,:])
     dum3, x3,_ = plt.hist(mi01[i,:],bins,alpha=0.4,edgecolor='white',color='white')
     n33[i,:] = dum3
     ag33[i] = np.nanmean(mi01[i,:])
     dum4, x4,_ = plt.hist(li01[i,:],bins,alpha=0.4,edgecolor='white',color='white')
     n44[i,:] = dum4
     ag44[i] = np.nanmean(li01[i,:])

minn22, maxn22 = np.nanmin(n22,0), np.nanmax(n22,0)
minn33, maxn33 = np.nanmin(n33,0), np.nanmax(n33,0)
minn44, maxn44 = np.nanmin(n44,0), np.nanmax(n44,0)

mn2 = np.nanmean(n22,0)
mn3 = np.nanmean(n33,0)
mn4 = np.nanmean(n44,0)
ax1.plot(bin_centers1, mn4,color='deepskyblue',alpha=1,label='SPEAR-LO',linewidth=2.5)
ax1.fill_between(bin_centers1, minn44, maxn44,facecolor='deepskyblue',alpha=0.2)
ax1.plot(bin_centers1, mn3,color='springgreen',alpha=1,label='SPEAR-MED',linewidth=2.5)
ax1.fill_between(bin_centers1, minn33, maxn33,facecolor='springgreen',alpha=0.2)
ax1.plot(bin_centers1, mn2,color='red',alpha=1,label='SPEAR-HI',linewidth=2.5)
ax1.fill_between(bin_centers1, minn22, maxn22,facecolor='red',alpha=0.2)
ax1.plot(bin_centers1, n1, color='black',alpha=1,label='ERA5',linewidth=2.5)

plt.legend(loc='upper left', title='ERA5 vs. Ensemble Mean',title_fontsize=16,fontsize=15)
plt.yticks(yticks)
ax = plt.gca()
ax.set_ylim(0,120)  # set y limit
ax.set_xlim(0,75)  # set x limit
ax.tick_params(axis='both',labelsize=16)
ax.set_ylabel("Frequency", fontsize = 20)
ax.set_xlabel("Maximum Intensity (mb)", fontsize= 20)
ax.set_title("Bomb Cyclone Maximum Intensity", fontsize= 20)
plt.tight_layout()
plt.show()

