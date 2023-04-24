import cv2
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import mplsoccer
""""
path = os.path.abspath(".")
loaded_arr = np.load(path+'\projetao\points.npy')
#print(loaded_arr)
new_arr= np.reshape(loaded_arr,(11,2))
#print(new_arr)
# convert array into dataframe
DF = pd.DataFrame(new_arr)
 
# save the dataframe as a csv file
DF.to_csv("position_data.csv")
"""

df = pd.read_csv('position_data.csv')
#print(df['0'])
x = df['0'].values/10
y = df['1'].values/10
print(x)
print(y)
pitch = mplsoccer.VerticalPitch(pitch_type='opta',pitch_color='green',pitch_length=231,pitch_width=144.8,line_color='black' ) 
fig, ax = pitch.draw(figsize=(16,10))
pitch.kdeplot(x,y, ax=ax,cmap='Reds',)


"""
bin_statistic = pitch.bin_statistic(y, x, statistic='count', bins=(50, 50))
bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
"""
plt.show()