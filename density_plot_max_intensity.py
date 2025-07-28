import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import norm
import seaborn as sns
dir_filtered = '/archive/Jessica.Hampson'
filtered_file = os.path.join(dir_filtered, 'output_NovtoMar_bomb_cyclone_tracks.npz')
filtered_file2 = os.path.join(dir_filtered, 'output_NovtoMar_filtered_cyclones_final.npz')
filtered = np.load(filtered_file)
filtered_reg2 = np.load(filtered_file2)
# max intensity code - all bomb cyclones 
track_id = filtered['xbcyc_ti00']
track_lifetime = filtered['xbcyc_num00']
track_int = filtered['xbcyc_int00']
bmax_intensity = []
for i in range(len(track_id)):
    idx = np.where(track_lifetime == track_id[i])[0]
    bcyc_int = track_int[idx]

    if bcyc_int.size > 0:
        bmax_int = np.max(bcyc_int)
        bmax_intensity.append(bmax_int)
# max intensity - all cyclones 
track_id2 = filtered_reg2['ext_ti00']
track_lifetime2 = filtered_reg2['ext_num00']
track_int2 = filtered_reg2['ext_revc00']
max_intensity = []
for i in range(len(track_id2)):
    idx2 = np.where(track_lifetime2 == track_id2[i])[0]
    cyc_int = track_int2[idx2]

    if cyc_int.size > 0:
        max_int = np.max(cyc_int)
        max_intensity.append(max_int)
sns.histplot(bmax_intensity,kde=True,stat='density', bins= list(range(0,70,20)), color='darkred', edgecolor='black',label= 'Bomb Cyclones',alpha=0.6,zorder=3)

sns.histplot(_max_intensity,kde=True,stat='density',bins= list(range(0,70,20)), color='blue',edgecolor='black',label='All Cyclones',alpha=0.6,zorder=3)

plt.xlabel('Maximum Intensity (mb)',fontsize=21)
plt.ylabel('Probability Density',fontsize=21)
plt.title('Maximum Intensity (Nov-Mar 1991-2020)',fontsize=22)
plt.legend(title='Cyclone Type',title_fontsize=18,fontsize=17)
plt.tick_params(axis='both',labelsize=17)
plt.grid(True)
plt.show()
