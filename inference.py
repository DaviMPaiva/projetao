import cv2
import time
from old_pipeline.object_detection import ObjectDetection
import matplotlib.pyplot as plt
import numpy as np
import threading
import pickle
import json
from old_pipeline.tracker import Tracker
from player import Player

class Inference(threading.Thread):
    def __init__(self, path1, path2,data,vs1,vs2,isStream):
        threading.Thread.__init__(self)
        self.path1 = path1
        self.path2 = path2
        # Initialize Object Detection
        self.od = ObjectDetection()
        #Init tracker
        self.tracker = Tracker()
        self.data = data
        self.vs1 = vs1
        self.vs2 = vs2
        self.isStream = isStream

    def GetInference(self,frame_rec):
            center_points_cur_frame = []
            
            # Detect objects on frame
            (class_ids, scores, boxes) = self.od.detect(frame_rec)

            detections = []

            for class_id, score, box in zip(class_ids, scores, boxes):
                if self.od.classes[class_id] == 'person':    
                    #print('class id = ', od.classes[class_id])
                    (x, y, w, h) = box

                    #print("FRAME N°", count, " ", x, y, w, h)

                    x1 = int(x)
                    x2 = int(x+w)
                    y1 = int(y)
                    y2 = int(y+h)
                    
                    # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    detections.append([x1, y1, x2, y2, score])

            if len(detections) != 0:
                self.tracker.update(frame_rec, detections)
                    
                ids = []
                for track in self.tracker.tracks:
                    bbox = track.bbox
                    x1, y1, x2, y2 = bbox
                    track_id = track.track_id

                    cx = int((x1 + x2)/2)
                    by = int(y2)

                    ids.append({"point":(cx,by),"id":track_id})

                    cv2.rectangle(frame_rec, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                    #cv2.circle(frame_rec, (cx,by), 5, (0, 0, 255), -1)
                    #cv2.putText(frame_rec, str(track_id), (cx, cy - 7), 0, 1, (0, 0, 255), 2)
                    
                
                cv2.imshow("Frame", frame_rec)
                return ids
            else:
                #cv2.imshow("Frame", frame_rec)
                return []
    
    def GetCorners(self,img):
        height, width, _ = img.shape
        # Resize the image to half its original size
        #img = cv2.resize(img, (int(width/2), int(height/2)))
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

    def GetConvertedCoor(self,corners,point):
        # convert the record 2d point to a select 2d 
        # Define the dimensions of the futsal img shape
        rect_width = 1000
        rect_height = 1600/2 #divide by 2 because whe are only using half the pitch
        corners_array = np.array(corners['points'], dtype=np.float32)
        # Define the corners of the rectangular shape
        rect_pts = np.array([[0, 0], [rect_width, 0], [rect_width, rect_height], [0, rect_height]], dtype=np.float32)

        M = cv2.getPerspectiveTransform(src=corners_array, dst=rect_pts)
        i = np.array([point], dtype=np.float32)
        i = i.reshape(-1, 1, 2)  # reshape to (1, 1, 2)
        transformed_point = cv2.perspectiveTransform(i, M)
        
        return transformed_point

    def GetImgCorners(self):
        return self.frame_corner1, self.frame_corner2

    def run(self) -> None:
        # Set up video capture
        capture1 = cv2.VideoCapture(self.path1)
        frame_rate_1 = capture1.get(cv2.CAP_PROP_FPS)

        capture2 = cv2.VideoCapture(self.path2)
        frame_rate_2 = capture2.get(cv2.CAP_PROP_FPS)

        print('FRAME RATE 1 : ', frame_rate_1)
        print('FRAME RATE 2', frame_rate_2)
        # Set up variables for timing
        prev_time = 0
        interval = 1

        ids_frames = []
        corners1 = []
        corners2 = []

        frame_counter = 0
        while True:

            if frame_counter % 3 != 0:
                frame_counter += 1
                continue

            # Read frame from video stream
            if self.isStream:
                ret1, frame1 = self.vs1.read()#capture1.read()
                ret2, frame2 = self.vs2.read()#capture1.read()
            else:
                ret1, frame1 = capture1.read()
                ret2, frame2 = capture2.read()  

            # Check if frame was successfully read
            if not ret2 or not ret1:
                continue #if there is a missing frame

            current_time1 = time.time()

            height = 720
            width = 1280
            
            #ask for the four points
            if(frame_counter==0):
                image1_resized = cv2.resize(frame1, (width, height))
                image2_resized = cv2.resize(frame2, (width, height))
                corners1 = self.GetCorners(image1_resized)
                corners2 = self.GetCorners(image2_resized)
                #self.frame_corner1 = image1_resized
                #self.frame_corner2 = image2_resized

            final_frame = []
            # Check if enough time has passed to use the frame
            if (current_time1 - prev_time) >= interval:
                print("resizing image")
                # Resize the images to the same height
                
                image1_resized = cv2.resize(frame1, (width, height))
                image2_resized = cv2.resize(frame2, (width, height))
                # Combine the two images side-by-side
                frame = cv2.vconcat([image1_resized, image2_resized])

                print("making inference")
                ids_frame = self.GetInference(frame)
                print("inference made")
                
                if(ids_frame != [] and ids_frame != None):
                    for frame in ids_frame:
                        if frame["point"][1] < height: #to be confirmed
                            coord = self.GetConvertedCoor(corners1,frame["point"])
                            x, y = coord[0, 0]
                            print([x,y])
                            final_frame.append({"point":[x,y],"id":frame["id"],"frame_num":frame_counter})
                        else:
                            frame_cor = (frame["point"][0],frame["point"][1]-height)
                            coord = self.GetConvertedCoor(corners2,frame_cor)
                            x, y = coord[0, 0]
                            print([x,y])
                            final_frame.append({"point":[x,y],"id":frame["id"],"frame_num":frame_counter}) 

                    #print(final_frame)
                    self.data.append_to_frame(final_frame)

                # Update previous time
                prev_time = current_time1

            
            frame_counter += 1
            # Check for 'q' key to quit
            if cv2.waitKey(1) == ord('q'):
                break

        # Release resources
        capture1.release()
        capture2.release()
        cv2.destroyAllWindows()

class Data:
    def __init__(self,lock):
        # Create the final_frame array as a private variable
        self.final_frame = []
        self.lock = lock

    def append_to_frame(self, data) -> None:
        # Acquire the lock
        self.lock.acquire()

        try:
            # Modify the array
            self.final_frame += (data)
            #print("writing value")
        finally:
            # Release the lock
            self.lock.release()

    def read_frame(self) -> None:
        # Acquire the lock
        self.lock.acquire()

        try:
            # Return a copy of the array
            print("returning value")
            return self.final_frame
        finally:
            # Release the lock
            self.lock.release()

class Consumer(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data
        self.players:dict[Player] = dict()
        self.last_worked_frame:int = 0


    def update_players(self):
        print('updating players')
        player_ids = self.players.keys() 
        player_ids = [id for id in player_ids]

        fresh_data = [d for d in self.data.read_frame() if d['frame_num'] > self.last_worked_frame]
        print(fresh_data)
        for data in fresh_data:
            coords = data['point']
            player_id = str(data['id'])
            #print(player_id)
            if player_id not in player_ids:
                self.players[player_id] = Player(player_id)
            
            self.players[player_id].update_coords_buffer(coords)
            self.players[player_id].update_tot_distance(field_width=8, field_height=7, screen_width=1280, screen_height=720)    
            self.players[player_id].instant_speed(field_width=8, field_height=7, screen_width=1280, screen_height=720, frame_time = 1)
        try:
            self.last_worked_frame = fresh_data[-1]['frame_num']
        except:
            pass
        #print(self.last_worked_frame)

    def test(self):
        return self.data.read_frame()

    def GetHeatmap(self) -> None:

        temp = self.data.read_frame()
        print(type(temp))
        if len(temp)>0:print(temp[0])
        points_array_x = [item['point'][0] for item in temp]
        points_array_y = [item['point'][1] for item in temp]
        plt.scatter(points_array_x, points_array_y)
        plt.xlim([0, 1000])
        plt.ylim([0, 800])
        # Set the title and labels for the plot
        plt.title('Scatter Plot of Data')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')

        plt.show()

        """
        # Load the background image
        bg = plt.imread('futsal.png')
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
        heatmap, xedges, yedges = np.histogram2d(points_array_x, points_array_y, bins=50, range=[[xmin, xmax], [ymin, ymax]])

        # Plot the heatmap using imshow function
        ax.imshow(heatmap.T, extent=[xmin, xmax, ymin, ymax], cmap='viridis', alpha=0.5)

        # Set the x and y axis limits
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        # Show the plot
        plt.show()
        """

class VideoStream:
    def __init__(self, url):
        self.url = url
        self.cap = cv2.VideoCapture(self.url)

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()


'''#video stream
vs1 = VideoStream('https://192.168.1.5:8080/video')
vs2 = VideoStream('https://192.168.1.7:8080/video')

#create the lock
lock = threading.Lock()
data = Data(lock)

#create the producer
my_thread = Inference('videos/guga1.mp4', 'videos/guga2_flip.mp4', data,vs1,vs2,isStream=False)
my_thread.start()

#create the consumer
my_consumer = Consumer(data)
my_consumer.start()

while True:
    #try:
    print("trying to get heatmap")
    my_consumer.update_players()
    time.sleep(20)  # wait for 2 seconds before running the function again
    #except:
    #    print('passouuuuuu')
    #    pass
'''
