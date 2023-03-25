import cv2
import numpy as np
from object_detection import ObjectDetection
import math
import csv
import os
import time

from tracker import Tracker

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("videos/output_video.mp4")

# Get the height and width of the video
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

video_out_path = os.path.join('.', 'out.mp4')
cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'MP4V'), cap.get(cv2.CAP_PROP_FPS),
                          (width, height))

with open('video_dimentions.txt', 'w') as f:
    # Write the height and width to the file
    f.write("Video height: {}\n".format(height))
    f.write("Video width: {}\n".format(width))
f.close()

#Init tracker
tracker = Tracker()

counter = 0

#init file to write position data 
with open('position_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["x_pos", "y_pos", "id"])

    #start detection and tracking loop
    while True:
        ret, frame = cap.read()
        
        # skip some frames to increase performance
        counter = counter + 1
        if counter % 3 != 1:
            continue

        #start_time = time.time()
        
        if not ret:
            break

        # Point current frame
        center_points_cur_frame = []

        # cv2.circle(frame, (0, 0), 5, (0, 0, 255), -1)

        # Detect objects on frame
        (class_ids, scores, boxes) = od.detect(frame)

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
        
        tracker.update(frame, detections)
            
        for track in tracker.tracks:
            bbox = track.bbox
            x1, y1, x2, y2 = bbox
            track_id = track.track_id

            cx = int((x1 + x2)/2)
            cy = int((y1 + y2)/2)

            # store position data  
            writer.writerow([cx, by, track_id])
           
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            cv2.circle(frame, (cx,cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, str(track_id), (cx, cy - 7), 0, 1, (0, 0, 255), 2)
        
        cv2.imshow("Frame", frame)
        
        #end_time = time.time() - start_time
        #print(end_time)
        
        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

file.close()