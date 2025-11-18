# cake_pop_demon_hunters
A motion-controlled webcam game built with Python and OpenCV where you hunt demons using cake pop movements and face tracking.

Features
- Mirrored Webcam Display: Natural mirror-like interaction
- Face Tracking: Real-time face detection with visual feedback
- Motion Detection: Destroy demons by waving your hands near them
- Corner Demons: Red demons spawn periodically in screen corners
- Falling Demon: Blue demon falls from top, avoid it or lose
- Score Tracking: Real-time score display
- Background Music: K-Pop soundtrack plays during gameplay
- Welcome Screen: 10-second countdown with setup instructions
- Game Over Screen: Final score display

How to Play
- Setup: Position yourself in front of your webcam with a still background
- Wait: 10-second countdown gives you time to get ready
- Destroy Corner Demons: Wave your cake pop at RED demons in the corners to destroy them
- Avoid Falling Demon: Don't let the BLUE demon touch your face
- Score Points:
  - +1 point for each corner demon destroyed
  - +5 points when falling demon exits bottom safely
  - Quit Anytime: Press 'Q' to exit
 
How It Works
- Face Detection: Uses OpenCV's Haar Cascade classifier to detect and track faces in real-time.
- Motion Detection: Compares consecutive frames to calculate pixel differences in demon regions. When motion exceeds a threshold, the demon is destroyed.
- Collision Detection: Uses Axis-Aligned Bounding Box algorithm to detect when the falling demon rectangle intersects with the face rectangle

By Mariela Mulready
