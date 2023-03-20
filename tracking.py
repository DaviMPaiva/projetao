import cv2
import numpy as np
from object_detection import ObjectDetection
import math
import csv

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("output_video.mp4")

# Get the height and width of the video
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

with open('video_dimentions.txt', 'w') as f:
    # Write the height and width to the file
    f.write("Video height: {}\n".format(height))
    f.write("Video width: {}\n".format(width))
f.close()

# Initialize count
count = 0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0

#init file to write position data 
with open('position_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["x_pos", "y_pos"])

    #start detection and tracking loop
    while True:
        ret, frame = cap.read()
        count += 1
        if not ret:
            break

        # Point current frame
        center_points_cur_frame = []

        cv2.circle(frame, (0, 0), 5, (0, 0, 255), -1)

        # Detect objects on frame
        (class_ids, scores, boxes) = od.detect(frame)
        for class_id, score, box in zip(class_ids, scores, boxes):
            if od.classes[class_id] == 'person':    
                print('class id = ', od.classes[class_id])
                (x, y, w, h) = box
                cx = int((x + x + w) / 2)
                cy = int((y + y + h) / 2)
                by = int(y + h)

                center_points_cur_frame.append((cx, cy))
                #print("FRAME N°", count, " ", x, y, w, h)

                # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # store position data  
                writer.writerow([cx, by])
                

        # Only at the beginning we compare previous and current frame
        if count <= 2:
            for pt in center_points_cur_frame:
                for pt2 in center_points_prev_frame:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                    if distance < 10:
                        tracking_objects[track_id] = pt
                        track_id += 1
        else:

            tracking_objects_copy = tracking_objects.copy()
            center_points_cur_frame_copy = center_points_cur_frame.copy()

            for object_id, pt2 in tracking_objects_copy.items():
                object_exists = False
                for pt in center_points_cur_frame_copy:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                    # Update IDs position
                    # isso aqui da problema na nossa detecção
                    # tem que ser uma comparação de distâncias mais eficiente
                    if distance < 20:
                        tracking_objects[object_id] = pt
                        object_exists = True
                        if pt in center_points_cur_frame:
                            center_points_cur_frame.remove(pt)
                        continue

                # Remove IDs lost
                if not object_exists:
                    tracking_objects.pop(object_id)

            # Add new IDs found
            for pt in center_points_cur_frame:
                tracking_objects[track_id] = pt
                track_id += 1

        for object_id, pt in tracking_objects.items():
            cv2.circle(frame, pt, 5, (0, 0, 255), -1)
            cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)

        print("Tracking objects")
        print(tracking_objects)


        print("CUR FRAME LEFT PTS")
        print(center_points_cur_frame)


        cv2.imshow("Frame", frame)

        # Make a copy of the points
        center_points_prev_frame = center_points_cur_frame.copy()

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

file.close()