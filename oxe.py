import cv2
import numpy as np

# Load the image
img = cv2.imread('X1.png')

# Define the corners of the quadrilateral
quad_pts = np.float32([(400, 44), (792, 53), (894, 418), (248, 409)])

# Define the dimensions of the rectangular shape
rect_width = 400
rect_height = 600

# Define the corners of the rectangular shape
rect_pts = np.float32([[0, 0], [rect_width, 0], [rect_width, rect_height], [0, rect_height]])

# Compute the perspective transform matrix
M = cv2.getPerspectiveTransform(quad_pts, rect_pts)

# Apply the perspective transformation to the image
rect_img = cv2.warpPerspective(img, M, (rect_width, rect_height))

# Display the result
cv2.imshow('rect_img', rect_img)
cv2.waitKey(0)