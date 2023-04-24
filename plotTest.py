
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mplsoccer.pitch import Pitch
import pandas as pd 
import ast


def column(matrix, i):
    return [row[i] for row in matrix]

df = pd.read_csv('pos.csv')
rows = []
for row in df['point']:
        rows.append(row)
points = []
for row in rows:
        points.append(ast.literal_eval(row))
#print(points)
#print(column(points,0))
points_array_x =column(points,0)
points_array_y = column(points,1)
p1x = []
p1y = []
p2x = []
p2y = []
id1 = []
id2 = []
for x in range(len(points)):
  if x % 2 ==0:
      p1x.append(points_array_x[x])
      p1y.append(points_array_y[x])
      id1.append(0)
  else:
      p2x.append(points_array_x[x])
      p2y.append(points_array_y[x])
      id2.append(1)
id = df['id']
p1x = [20+(i /12) for i in p1x]
p2x = [100-i /10 for i in p2x]
p1y = [i /16 for i in p1y]
p2y = [100-i /15 for i in p2y]
#pitch = Pitch(pitch_color='#4b4b4b', line_color='white',stripe_color='#646464',
#stripe=False,axis=True, label=True)
#fig, ax = pitch.draw(figsize=(7, 4))
#pitch.kdeplot(np.concatenate((p1y, p2y)), np.concatenate((p1x, p2x)), ax=ax,fill=True,cmap='Reds',zorder=1)
#pitch.scatter( np.concatenate((p1y, p2y)), np.concatenate((p1x, p2x)), c = np.concatenate((id1, id2)), cmap='gray',s=80, ec='k', ax=ax)

pitch = Pitch(pitch_type='opta',pitch_color='black',line_color='white',line_zorder=2)
fig, ax = pitch.draw(figsize=(7, 4))
fig.set_facecolor('black')
customcmap= matplotlib.colors.LinearSegmentedColormap.from_list('custom cmap',['black','red'])
pitch.kdeplot(np.concatenate((p1y, p2y)), np.concatenate((p1x, p2x)), ax=ax,fill=True,cmap=customcmap,zorder=1,n_levels=100)
#pitch.scatter( np.concatenate((p1y, p2y)), np.concatenate((p1x, p2x)), c = np.concatenate((id1, id2)), cmap='gray',s=80, ec='k', ax=ax)
plt.show()

