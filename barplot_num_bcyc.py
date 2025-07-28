# script to create bar plot for the 5 ensemble member mean value for each SPEAR res 
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

dir_filtered = '/archive/Jessica.Hampson'
ERA5 = os.path.join(dir_filtered, 'output_NovtoMar_bomb_cyclone_tracks.npz')

med_ens01 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-MED_ens01.npz')
med_ens02 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-MED_ens02.npz')
med_ens03 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-MED_ens03.npz')
med_ens04 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-MED_ens04.npz')
med_ens05 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-MED_ens05.npz')

hi_ens01 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-HI_ens01.npz')
hi_ens02 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-HI_ens02.npz')
hi_ens03 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-HI_ens03.npz')
hi_ens04 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-HI_ens04.npz')
hi_ens05 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-HI_ens05.npz')

lo_ens01 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-LOW_ens01.npz')
lo_ens02 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-LOW_ens02.npz')
lo_ens03 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-LOW_ens03.npz')
lo_ens04 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-LOW_ens04.npz')
lo_ens05 = os.path.join(dir_filtered, 'bomb_cyc_NovtoMar_SPEAR-LOW_ens05.npz')

ERA5 = np.load(ERA5)
mens01 = np.load(med_ens01)
mens02 = np.load(med_ens02)
mens03 = np.load(med_ens03)
mens04 = np.load(med_ens04)
mens05 = np.load(med_ens05)

hens01 = np.load(hi_ens01)
hens02 = np.load(hi_ens02)
hens03 = np.load(hi_ens03)
hens04 = np.load(hi_ens04)
hens05 = np.load(hi_ens05)

lens01 = np.load(lo_ens01)
lens02 = np.load(lo_ens02)
lens03 = np.load(lo_ens03)
lens04 = np.load(lo_ens04)
lens05 = np.load(lo_ens05)

ERA5_id = ERA5['xbcyc_ti00']
mens01_id = mens01['xsmb_ti00']
mens02_id = mens02['xsmb_ti00']
mens03_id = mens03['xsmb_ti00']
mens04_id = mens04['xsmb_ti00']
mens05_id = mens05['xsmb_ti00']

hens01_id = hens01['xshb_ti00']
hens02_id = hens02['xshb_ti00']
hens03_id = hens03['xshb_ti00']
hens04_id = hens04['xshb_ti00']
hens05_id = hens05['xshb_ti00']

lens01_id = lens01['xslb_ti00']
lens02_id = lens02['xslb_ti00']
lens03_id = lens03['xslb_ti00']
lens04_id = lens04['xslb_ti00']
lens05_id = lens05['xslb_ti00']

#store total # of bomb cyc per ens
ERA5_num = len(ERA5_id)
mens1_num = len(mens01_id)
mens2_num = len(mens02_id)
mens3_num = len(mens03_id)
mens4_num = len(mens04_id)
mens5_num = len(mens05_id)

hens1_num = len(hens01_id)
hens2_num = len(hens02_id)
hens3_num = len(hens03_id)
hens4_num = len(hens04_id)
hens5_num = len(hens05_id)

lens1_num = len(lens01_id)
lens2_num = len(lens02_id)
lens3_num = len(lens03_id)
lens4_num = len(lens04_id)
lens5_num = len(lens05_id)

# plot 
mcounts = [mens1_num,  mens2_num, mens3_num, mens4_num, mens5_num]
med_mean_ens = np.mean([mens1_num,  mens2_num, mens3_num, mens4_num, mens5_num]
)

hcounts = [hens1_num,  hens2_num, hens3_num, hens4_num, hens5_num]
hi_mean_ens = np.mean([hens1_num,  hens2_num, hens3_num, hens4_num, hens5_num]
)

lcounts = [lens1_num,  lens2_num, lens3_num, lens4_num, lens5_num]
lo_mean_ens = np.mean([lens1_num,  lens2_num, lens3_num, lens4_num, lens5_num])

hi_std_ens = np.std([hens1_num,  hens2_num, hens3_num, hens4_num, hens5_num])
med_std_ens = np.std([mens1_num,  mens2_num, mens3_num, mens4_num, mens5_num])
lo_std_ens = np.std([lens1_num,  lens2_num, lens3_num, lens4_num, lens5_num])
era5_std_ens = 0
era5 = ERA5_num


labels=['ERA5','HI', 'MED', 'LO']
colors= ['black','firebrick','darkorange','deepskyblue']
values=[era5, hi_mean_ens, med_mean_ens, lo_mean_ens]
error = [np.nan, hi_std_ens,med_std_ens,lo_std_ens]

plt.figure(figsize=(8,7))
bars = plt.bar(x=labels,height=values,color=colors, width=0.5, yerr=error,capsize=8)
for i, bar in enumerate(bars):
    height = bar.get_height()
    offset = error[i] if error[i] > 0 else 0  # avoid adding 0 if there's no error
    plt.text(bar.get_x() + bar.get_width() / 2., height + offset + 2, f'{int(height)}',
             ha='center', va='bottom', fontsize=16.5)

plt.xlabel('ERA5 vs. HI/MED/LO Resolution', fontsize=19)
plt.ylabel('Frequency of Bomb Cyclones', fontsize=19)
plt.title('Total Bomb Cyclones', fontsize=20)
plt.xticks(fontsize=16)
plt.ylim(220,315)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.legend()
plt.show()
