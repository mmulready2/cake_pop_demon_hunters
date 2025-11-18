print("This is mirror.py")

import numpy as np
import cv2 as cv
import time, random

score = 0
game_over = False
game_over_message = ""
show_instructions = True  
instruction_start_time = time.time() 

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

# Falling demon
falling_demon = None
last_falling_spawn = time.time()
falling_spawn_interval = 5.0
falling_speed = 20

# Functions
def spawn_corner_demon(width, height):
    positions = [
        (0, 0),                          # Top Left
        (width - 300, 0),                # Top Right  
        (0, height - 300),               # Bottom Left
        (width - 300, height - 300)      # Bottom Right
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

def spawn_falling_demon(width):
    return {'x': width // 2 - 50, 'y': 0, 'width': 100, 'height': 150, 'active': True}

def check_collision(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

# Mirror
first = True
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Flip
    frame = cv.flip(frame,1)
    height = frame.shape[0]
    width  = frame.shape[1]

    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if first:
        prev_gray = gray
        first = False

    # Makes mirror not stop when a point is scored
    if not game_over:
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        face_rect = None
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            face_rect = (x, y, w, h)
            break

        # Spawn in demons at time
        current_time = time.time()
        if current_time - last_corner_spawn > corner_spawn_interval:
            spawn_corner_demon(width, height)
            last_corner_spawn = current_time

        # Spawn falling demon
        if current_time - last_falling_spawn > falling_spawn_interval:
            if falling_demon is None or not falling_demon['active']:
                falling_demon = spawn_falling_demon(width)
                last_falling_spawn = current_time

        # Corner demons
        for demon in corner_demons[:]:
            if demon['active']:
                # Check motion and show the amount
                motion_amount = 0
                h, w = gray.shape
                x1, y1 = max(0, demon['x']), max(0, demon['y'])
                x2, y2 = min(w, demon['x'] + demon['width']), min(h, demon['y'] + demon['height'])
                if x1 < x2 and y1 < y2:
                    motion_amount = cv.absdiff(gray[y1:y2, x1:x2], prev_gray[y1:y2, x1:x2]).sum()
                
                if check_motion_in_area(gray, prev_gray, demon['x'], demon['y'], demon['width'], demon['height']):
                    demon['active'] = False
                    score += 1
                    corner_demons.remove(demon)
                    continue
                # Draw as filled red rectangle (replaces your original gray rectangles)
                cv.rectangle(frame, (demon['x'], demon['y']), 
                           (demon['x'] + demon['width'], demon['y'] + demon['height']), (0, 0, 255), -1)
                cv.putText(frame, "DEMON", (demon['x'] + 80, demon['y'] + 180),
                         cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
                # Show motion amount for debugging
                cv.putText(frame, f"{int(motion_amount/1000)}K", (demon['x'] + 10, demon['y'] + 30),
                         cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Update falling demon
    if falling_demon and falling_demon['active']:
        falling_demon['y'] += falling_speed
        
        if face_rect:
            demon_rect = (falling_demon['x'], falling_demon['y'], falling_demon['width'], falling_demon['height'])
            if check_collision(face_rect, demon_rect):
                game_over = True
                game_over_message = "GAME OVER! Demon Hit Your Face!"
        
        if falling_demon['y'] > height:
            score += 5
            falling_demon = None
        else:
            cv.rectangle(frame, (falling_demon['x'], falling_demon['y']), (falling_demon['x'] + falling_demon['width'], falling_demon['y'] + falling_demon['height']), (255, 0, 0), -1)
            cv.putText(frame, "DEMON", (falling_demon['x'] + 5, falling_demon['y'] + 90), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if face_rect:
                fx, fy, fw, fh = face_rect
                dx, dy, dw, dh = falling_demon['x'], falling_demon['y'], falling_demon['width'], falling_demon['height']
                # Show collision warning when close
                if dy + dh > fy and dy < fy + fh and abs((fx + fw//2) - (dx + dw//2)) < 150:
                    cv.putText(frame, "CLOSE!", (width//2 - 80, height//2 - 100),cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 165, 255), 3)

    # Calculate change in gray
    delta = cv.absdiff(gray[0:100],prev_gray[0:100]).sum()

    # Display text
    cv.putText(frame, str(int(delta)), (50, height - 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show threshold
    cv.putText(frame, f"Threshold: {motion_threshold/1000}K", (50, height - 100),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Display score
    cv.putText(frame, f"Score: {score}", (width//2 - 100, 60), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    # Instructions
    if show_instructions:
        time_remaining = int(10 - (time.time() - instruction_start_time))
        
        overlay = frame.copy()
        cv.rectangle(overlay, (width//2 - 400, 100), (width//2 + 400, 320), (0, 0, 0), -1)
        cv.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv.putText(frame, "DEMON HUNTER - GET READY!", (width//2 - 380, 150),
                 cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)
        cv.putText(frame, "Ensure NO movement behind you", (width//2 - 360, 195),
                 cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv.putText(frame, "Use a blank/still background", (width//2 - 340, 235),
                 cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv.putText(frame, "Wave hands at RED demons to destroy", (width//2 - 380, 275),
                 cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 100, 100), 2)
        
        # Countdown
        cv.putText(frame, f"Starting in: {time_remaining}", (width//2 - 150, 315),
                 cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # Display game over
    if game_over:
        cv.putText(frame, game_over_message, (width//2 - 400, height//2),
                 cv.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)
        cv.putText(frame, f"Final Score: {score}", (width//2 - 250, height//2 + 80),
                 cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
        cv.putText(frame, "Press Q to Exit", (width//2 - 220, height//2 + 150),
                 cv.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)

    # Display resulting frame
    cv.imshow('frame', frame)

    # Save prev gray
    prev_gray = gray

    # See if user wants to quit
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()




