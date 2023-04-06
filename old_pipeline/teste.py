import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Read the CSV file into a pandas dataframe
df = pd.read_csv('position_data.csv')

# Extract the x and y coordinates into separate arrays
x = df['x_pos'].values
y = df['y_pos'].values

# Create a scatter plot of the data
plt.scatter(x, y)

# Set the title and labels for the plot
plt.title('Scatter Plot of Data')
plt.xlabel('X Position')
plt.ylabel('Y Position')

# Set the range for the x and y axes
plt.xlim(0, 400)
plt.ylim(600, 0)

# Show the plot
plt.show()

