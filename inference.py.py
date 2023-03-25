import cv2
import time
from object_detection import ObjectDetection
import matplotlib.pyplot as plt
import numpy as np

# Initialize Object Detection
od = ObjectDetection()

from tracker import Tracker

#Init tracker
tracker = Tracker()

def GetInference(frame_rec):
        center_points_cur_frame = []
        
        # Detect objects on frame
        (class_ids, scores, boxes) = od.detect(frame_rec)

        detections = []

        for class_id, score, box in zip(class_ids, scores, boxes):
            if od.classes[class_id] == 'person':    
                print('class id = ', od.classes[class_id])
                (x, y, w, h) = box
                cx = int((x + x + w) / 2)
                cy = int((y + y + h) / 2)
                by = int(y + h)

                center_points_cur_frame.append((cx, cy))
                #print("FRAME N°", count, " ", x, y, w, h)

                x1 = int(x)
                x2 = int(x+w)
                y1 = int(y)
                y2 = int(y+h)

                # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                detections.append([x1, y1, x2, y2, score])
        
        tracker.update(frame_rec, detections)
            
        ids = []
        for track in tracker.tracks:
            bbox = track.bbox
            x1, y1, x2, y2 = bbox
            #track_id = track.track_id

            cx = int((x1 + x2)/2)
            cy = int((y1 + y2)/2)

            ids.append((cx,cy))

            #cv2.rectangle(frame_rec, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            #cv2.circle(frame_rec, (cx,cy), 5, (0, 0, 255), -1)
            #cv2.putText(frame_rec, str(track_id), (cx, cy - 7), 0, 1, (0, 0, 255), 2)
        
        #cv2.imshow("Frame", frame_rec)
        return ids
 
def GetCorners(img):
    height, width, _ = img.shape
    # Resize the image to half its original size
    img = cv2.resize(img, (int(width/2), int(height/2)))
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
    return params

# Set up video capture
#capture = cv2.VideoCapture("http://192.168.1.67:8080/video")
capture = cv2.VideoCapture('video_test_tiny.mp4')

# Set up variables for timing
prev_time = 0
interval = 56

ids_frames = []
corners = {'points': 0}

while True:
    # Read frame from video stream
    ret, frame = capture.read()
    
    # Check if frame was successfully read
    if not ret:
        break
    current_time = capture.get(cv2.CAP_PROP_POS_MSEC)
    #ask for the four points
    if(current_time==0):
        corners = GetCorners(frame)
                  
    # Check if enough time has passed to save frame
    if (current_time - prev_time) >= interval:

        ids_frames.append(GetInference(frame))
        # Update previous time
        prev_time = current_time


    # Display frame on screen

    # Check for 'q' key to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
capture.release()
cv2.destroyAllWindows()

#convert the record 2d point to a select 2d 
# Define the dimensions of the rectangular shape
rect_width = 1000
rect_height = 1600/2 #divide by 2 because whe are only using half the pitch
corners_array = np.array(corners['points'], dtype=np.float32)

points = []

for i in ids_frames:
    if i == []:
        continue
    # Define the corners of the rectangular shape
    rect_pts = np.array([[0, 0], [rect_width, 0], [rect_width, rect_height], [0, rect_height]], dtype=np.float32)
    
    M = cv2.getPerspectiveTransform(src=corners_array, dst=rect_pts)
    transformed_point = cv2.perspectiveTransform(np.array([i], dtype=np.float32), M)
    points.append(transformed_point)

print(points)

np.save("points", points)

#how to load:
# load the array from the file
#loaded_arr_4d = np.load('arr_4d.npy')

# check that the loaded array is the same as the original array
#assert np.array_equal(arr_4d, loaded_arr_4d)