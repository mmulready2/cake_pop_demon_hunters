print("This is mirror.py")

import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

first = True
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # turn the image into mirror image
    frame = cv.flip(frame,1)
    height, width = frame.shape[:2]

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if first:
        prev_gray = gray
        first = False

    # Calculate change in gray
    delta = cv.absdiff(gray[0:100],prev_gray[0:100]).sum()
    cv.rectangle(frame, (0,0), (100,100),(100,100,100),2)

    # Display text
    cv.putText(frame, str(delta), (50,300), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)
    cv.putText(frame, "Demon", (100,100), cv.FONT_HERSHEY_SIMPLEX, 2, (150,0,150), 5)

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




