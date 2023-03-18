import cv2
import os

# Set the path to the folder containing the frames
folder_path = 'frames_after'

# Set the frame rate (frames per second)
frame_rate = 30

# Set the output video file name
output_filename = 'output_video.mp4'

list_imgs =  os.listdir(folder_path)
integers = [int(s.split(".")[0]) for s in list_imgs]
sorted_integers = sorted(integers)
sorted_strings = [str(str(i)+".jpg") for i in sorted_integers]
#print(sorted_strings)

# Get the dimensions of the first frame to use for the video
first_frame_path = os.path.join(folder_path,sorted_strings[0])
first_frame_path = first_frame_path
first_frame = cv2.imread(first_frame_path)
height, width, channels = first_frame.shape
dimensions = (width, height)

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_filename, fourcc, frame_rate, dimensions)

# Loop through the frames in the folder and add them to the video
for filename in sorted_strings:
    print(filename)
    # Load the frame
    frame_path = os.path.join(folder_path, filename)
    frame = cv2.imread(frame_path)
    
    # Write the frame to the video
    video_writer.write(frame)

# Release the video writer
video_writer.release()

# Print a message to indicate that the video has been saved
print(f'Video saved as {output_filename}')
