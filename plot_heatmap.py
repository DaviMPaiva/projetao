import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Read the CSV file into a pandas dataframe
df = pd.read_csv('position_data.csv')

# Extract the x and y coordinates into separate arrays
x = df['x_pos'].values/2 +100
y = df['y_pos'].values/2 + 350

# Load the background image
bg = plt.imread('campo_fut.jpg')
height, width, channels = bg.shape

# Define the range of the x and y coordinates
xmin, xmax =  (0,width)
ymin, ymax =  (0,height)

print("width: " + str(width) + " height: " + str(height))

# Create a figure with the same aspect ratio as the background image
fig, ax = plt.subplots(figsize=(bg.shape[1]/100,bg.shape[0]/100))

# Plot the background image
ax.imshow(bg)

# Convert the coordinates to a heatmap using the histogram2d function
heatmap, xedges, yedges = np.histogram2d(x, y, bins=50, range=[[xmin, xmax], [ymin, ymax]])

# Plot the heatmap using imshow function
ax.imshow(heatmap.T, extent=[xmin, xmax, ymin, ymax], cmap='viridis', alpha=0.5)

# Set the x and y axis limits
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Show the plot
plt.show()
