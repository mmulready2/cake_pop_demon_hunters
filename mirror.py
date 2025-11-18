print("This is mirror.py")

import numpy as np
import cv2 as cv
import time, random

score = 0

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Face detection
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# Corner demon variables
corner_demons = []
last_corner_spawn = time.time()
corner_spawn_interval = 3.0
motion_threshold = 500000

# Functions
def spawn_corner_demon(width, height):
    positions = [
        (0, 0), (width - 300, 0),
        (0, height - 300), (width - 300, height - 300)
    ]
    pos = random.choice(positions)
    corner_demons.append({'x': pos[0], 'y': pos[1], 'width': 300, 'height': 300, 'active': True})

def check_motion_in_area(gray, prev_gray, x, y, width, height):
    h, w = gray.shape
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(w, x + width), min(h, y + height)
    if x1 >= x2 or y1 >= y2:
        return False
    delta = cv.absdiff(gray[y1:y2, x1:x2], prev_gray[y1:y2, x1:x2]).sum()
    return delta > motion_threshold

# Mirror
first = True
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # turn the image into mirror image
    frame = cv.flip(frame,1)
    height = frame.shape[0]
    width  = frame.shape[1]

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if first:
        prev_gray = gray
        first = False

    # More face detection
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        break

    # Spawn in demons at time
    current_time = time.time()
    if current_time - last_corner_spawn > corner_spawn_interval:
        spawn_corner_demon(width, height)
        last_corner_spawn = current_time

    # Corner demons check
    for demon in corner_demons[:]:
        if demon['active']:
            if check_motion_in_area(gray, prev_gray, demon['x'], demon['y'], demon['width'], demon['height']):
                demon['active'] = False
                score += 1
                corner_demons.remove(demon)
                continue
            cv.rectangle(frame, (demon['x'], demon['y']), 
                       (demon['x'] + demon['width'], demon['y'] + demon['height']), (0, 0, 255), -1)
            cv.putText(frame, "DEMON", (demon['x'] + 80, demon['y'] + 180),
                     cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Calculate change in gray
    delta = cv.absdiff(gray[0:100],prev_gray[0:100]).sum()
    # Top Left
    cv.rectangle(frame, (0, 0), (300, 300), (100,100,100), 2)
    # Top Right
    cv.rectangle(frame, (1500, 50), (1800, 350), (100,100,100), 2)
    # Bottom Left
    cv.rectangle(frame, (0, 1300), (300, 1600), (100,100,100), 2)
    # Bottom Right
    cv.rectangle(frame, (1500, 750), (1800, 1050), (100,100,100), 2)

    # Display text
    cv.putText(frame, str(delta), (50,300), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)
    # Top Left
    cv.putText(frame, "Demon", (100,100), cv.FONT_HERSHEY_SIMPLEX, 2, (150,0,150), 5)
    # Top Right
    cv.putText(frame, "Demon", (1600,100), cv.FONT_HERSHEY_SIMPLEX, 2, (150,0,150), 5)
    # Bottom Left
    cv.putText(frame, "Demon", (100,1000), cv.FONT_HERSHEY_SIMPLEX, 2, (150,0,150), 5)
    # Bottom Right
    cv.putText(frame, "Demon", (1600,1000), cv.FONT_HERSHEY_SIMPLEX, 2, (150,0,150), 5)

    # Display score
    cv.putText(frame, f"Score: {score}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    # Display resulting frame
    # cv.imshow('frame', gray)
    cv.imshow('frame', frame)

    # Save prev gray
    prev_gray = gray

    # See if user wants to quit
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()




