# from picamera2 import Picamera2
# print(Picamera2.global_camera_info())

from picamera2 import Picamera2
import time

try:
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
    picam2.start()
    time.sleep(2)  # Allow time for the camera to start
    frame = picam2.capture_array()
    print("Frame captured successfully!")
    picam2.stop()
except Exception as e:
    print(f"Camera error: {e}")
