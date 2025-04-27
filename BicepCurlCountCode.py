from picamera2 import Picamera2
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Start the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (1920, 1080)}))
picam2.start()

# Step 6: Define angle calculation function
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Step 7: Start counter
counter = 0
stage = None

while True:
    frame = picam2.capture_array()

    # Convert to RGB for MediaPipe
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw pose landmarks
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract landmarks for left arm
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

        # Get coordinates and calculate angle
        shoulder_coords = [left_shoulder.x, left_shoulder.y]
        elbow_coords = [left_elbow.x, left_elbow.y]
        wrist_coords = [left_wrist.x, left_wrist.y]
        angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

        # Bicep curl counter logic
        if angle > 160:
            stage = "Down"
        if angle < 30 and stage == "Down":
            stage = "Up"
            counter += 1

        # Display angle and count on the image
        cv2.putText(image, f'Elbow Angle: {int(angle)}', (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, f'Curls: {counter}', (10, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)

    # Resize and show image
    resized_frame = cv2.resize(image, (640, 480))
    cv2.imshow("Pose Detection", resized_frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.close()
