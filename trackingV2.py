import cv2
import os
import time
import requests

from object_detection import ObjectDetection
import plot_heatmap as hplot
from tracker import Tracker
from player import Player

#url to send heatmaps
URL = 'http://localhost:5000/heatmap'

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("videos\output_video.mp4")

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

#INIT TRACKER
tracker = Tracker()

counter = 0

'''#init file to write position data
coords_path_base = 'position_data_'
hmap_dir = './imgs/heatmap/'
coords_buffer = []
hplot.csv_init(coords_path)'''

players:dict[Player] = dict()

#START DETECTION AND TRACKING LOOP
while True:
    ret, frame = cap.read()
    start_time = time.time()

    # SKIP SOME FRAMES TO INCREASE PERFORMANCE
    counter = counter + 1
    if counter % 3 != 1:
        end_time = time.time() - start_time
        #print(end_time)
        continue
    
    if not ret:
        continue

    # DETECT OBJECTS ON FRAME
    (class_ids, scores, boxes) = od.detect(frame)

    detections = []

    for class_id, score, box in zip(class_ids, scores, boxes):
        if od.classes[class_id] == 'person':    
            #print('class id = ', od.classes[class_id])
            (x, y, w, h) = box

            x1 = int(x)
            x2 = int(x+w)
            y1 = int(y)
            y2 = int(y+h)

            detections.append([x1, y1, x2, y2, score])
    
    if len(detections) != 0:
        tracker.update(frame, detections) 
            
        for track in tracker.tracks:
            bbox = track.bbox
            x1, y1, x2, y2 = bbox
            track_id = track.track_id

            cx = int((x1 + x2)/2)
            cy = int((y1 + y2)/2)
            by = int(y2)
            
            # UPDATE PLAYERS
            try:
                coords = (cx, by, counter)
                players[str(track_id)].update_coords_buffer(coords)
                players[str(track_id)].update_tot_distance()
            except:
                players[str(track_id)] = Player(track_id)
                players[str(track_id)].update_coords_buffer(coords)
                players[str(track_id)].update_tot_distance()

            # STORE POSITION DATA
            #coords_buffer.append([cx, by, track_id])
            #hplot.append_coords(coords_path, [cx, by, track_id])
            
            #DRAW ON FRAME
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.circle(frame, (cx,cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, str(track_id), (cx, cy - 7), 0, 1, (0, 0, 255), 2)
        
    cv2.imshow("Frame", frame)

    if counter % 15 == 1: #update heatmap and send to server
        for key in players:
            players[key].update_coords_file()
            print(players[key].id, ' - ', players[key].tot_distance)

        #hplot.append_coords_list(coords_path, coords_buffer)
        #coords_buffer = []
        #img_name = hplot.plot_heatmap(coords_path, counter, hmap_dir)        
        #payload = {'img':img_name}
        
        #response = requests.post(URL, payload)
    
    #MEASURE TIME SPENT TO PROCESS FRAME
    end_time = time.time() - start_time
    #print(end_time)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()