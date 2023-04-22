import cv2
import time

url = 'https://192.168.1.5:8080/video'
cap = cv2.VideoCapture(url)

url = 'https://192.168.1.7:8080/video'
cap2 = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Unable to open camera")
    exit()

if not cap2.isOpened():
    print("Unable to open camera")
    exit()

while True:
    ret1, frame1 = cap.read()
    
    ret2, frame2 = cap2.read()
    if not ret1 or not ret2:
        print("Unable to read frame")
        break
    

    height = 360
    width = 1280

    # Display the smaller frame
    image1_resized = cv2.resize(frame1, (width, height))
    image2_resized = cv2.resize(frame2, (width, height))
    # Combine the two images side-by-side
    frame = cv2.vconcat([image1_resized, image2_resized])
    
    cv2.imshow('frame', frame)
    # Exit the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
