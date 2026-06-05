import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

class HandTracker:
    def __init__(self, max_hands=2, detection_conf=0.7, tracking_conf=0.5):
        model_path = "hand_landmarker.task"
        if not os.path.exists(model_path):
            print("Model download ho raha hai... wait karo")
            urllib.request.urlretrieve(
                "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
                model_path
            )
            print("Model download complete!")

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_conf,
            min_hand_presence_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.frame_timestamp = 0

        self.CONNECTIONS = [
            (0,1),(1,2),(2,3),(3,4),
            (0,5),(5,6),(6,7),(7,8),
            (0,9),(9,10),(10,11),(11,12),
            (0,13),(13,14),(14,15),(15,16),
            (0,17),(17,18),(18,19),(19,20),
            (5,9),(9,13),(13,17)
        ]

    def get_landmarks(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )
        self.frame_timestamp += 1
        result = self.detector.detect_for_video(mp_image, self.frame_timestamp)
        if result.hand_landmarks:
            return result.hand_landmarks
        return None

    def get_pixel_points(self, landmarks, w, h):
        points = []
        for lm in landmarks:
            points.append((int(lm.x * w), int(lm.y * h)))
        return points