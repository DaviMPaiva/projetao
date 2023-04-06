import cv2
import math
import numpy as np
import os

if not os.path.exists('frames_after'):
    os.makedirs('frames_after')

# Load the image
img = cv2.imread('frames/frame_0000.png')

# Create a window to display the image
cv2.namedWindow('image')


# Create a resizable window to display the image
cv2.namedWindow('image', cv2.WINDOW_NORMAL)


# Set the callback function for mouse events
def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(params['points']) < 4:
            print(f"({x}, {y})")
            params['points'].append((x, y))

            if len(params['points']) == 4:
                params['done'] = True


# Display the image and wait for mouse events
points = []
params = {'points': points, 'done': False}
cv2.imshow('image', img)
cv2.setMouseCallback('image', mouse_callback, params)

while True:
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouse_callback, params)
    key = cv2.waitKey(1) & 0xFF
    if params['done'] or key == 27: # break if 4 clicks or ESC key pressed
        break

cv2.destroyAllWindows()


folder_path = "frames"
# loop through every file in the folder
i = 0
for filename in os.listdir(folder_path):
    print(filename)
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # read the image
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)

        quad_pts = np.float32([params['points'][0], params['points'][1], params['points'][2], params['points'][3]])

        # Define the dimensions of the rectangular shape
        rect_width = 400
        rect_height = 600

        # Define the corners of the rectangular shape
        rect_pts = np.float32([[0, 0], [rect_width, 0], [rect_width, rect_height], [0, rect_height]])
        print("================================================")
        print(quad_pts)
        print("================================================")

        # Compute the perspective transform matrix
        M = cv2.getPerspectiveTransform(quad_pts, rect_pts)

        # Apply the perspective transformation to the image
        rect_img = cv2.warpPerspective(img, M, (rect_width, rect_height))

        cv2.imwrite("frames_after/" + str(i) + ".jpg", rect_img)
        i+=1

