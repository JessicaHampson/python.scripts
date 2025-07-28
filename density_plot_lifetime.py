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
#lifetime values - all bomb cyclones
track_id = filtered['xbcyc_ti00']
track_lifetime = filtered['xbcyc_num00']
lifetime = []
#convert to days 
for i in range(len(track_id)):
    idx = np.where(track_lifetime == track_id[i])[0]
    lifetime_days = len(idx) / 4
    lifetime.append(lifetime_days)
#lifetime for all cyclones 
track_id2 = filtered_reg2['ext_ti00']
track_lifetime2 = filtered_reg2['ext_num00']
lifetime2 = []
for i in range(len(track_id2)):
    idx2 = np.where(track_lifetime2 == track_id2[i])[0]
    lifetime_days2 = len(idx2) / 4
    lifetime2.append(lifetime_days2)
sns.histplot(lifetime,kde=True,stat='density', bins= list(range(2,15,1)), color='darkred', edgecolor='black',label= 'Bomb Cyclones',alpha=0.6,zorder=3)

sns.histplot(lifetime2,kde=True,stat='density',bins= list(range(2,15,1)), color='blue',edgecolor='black',label='All Cyclones',alpha=0.6,zorder=3)

plt.xlabel('Lifetime (days)',fontsize=21)
plt.ylabel('Probability Density',fontsize=21)
plt.title('Lifetime (Nov-Mar 1991-2020)',fontsize=22)
plt.legend(title='Cyclone Type',title_fontsize=18,fontsize=17)
plt.tick_params(axis='both',labelsize=17)
plt.grid(True)
plt.show()
