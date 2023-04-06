import cv2
import os

# Open the video file
cap = cv2.VideoCapture('videos\parte1.mp4')

# Create a directory to store the frames
if not os.path.exists('frames'):
    os.makedirs('frames')

# Initialize a counter variable
frame_count = 0

# Set the maximum width or height for resizing
max_size = 500

# Loop through the video frames
while True:
    # Read a frame from the video
    ret, frame = cap.read()
    
    # If there are no more frames, break out of the loop
    if not ret:
        break
    
    # Resize the frame while preserving aspect ratio
    height, width = frame.shape[:2]
    if height > width:
        ratio = max_size / height
    else:
        ratio = max_size / width
    new_size = (int(width * ratio), int(height * ratio))
    resized_frame = cv2.resize(frame, new_size)
    
    # Save the frame to a file
    filename = os.path.join('frames', f'frame_{frame_count:04d}.png')
    cv2.imwrite(filename, resized_frame)
    
    # Increment the counter variable
    frame_count += 1

# Release the video file and close the window
cap.release()
cv2.destroyAllWindows()
