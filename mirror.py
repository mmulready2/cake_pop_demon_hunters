print("This is mirror.py")

import numpy as np
import cv2 as cv
import time, random

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Face detection
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")


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




