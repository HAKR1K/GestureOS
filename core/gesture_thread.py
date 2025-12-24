from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage
import cv2
import mediapipe as mp
import numpy as np
import joblib


class GestureThread(QThread):
    frame_signal = pyqtSignal(QImage)
    status_signal = pyqtSignal(str)
    gesture_detected = pyqtSignal(str)

    def __init__(self, features=None):
        super().__init__()
        self.running = True

        # Load ML model
        self.model = joblib.load("gesture_model.pkl")
        self.scaler = joblib.load("gesture_scaler.pkl")

        self.THRESHOLDS = {

            "COPY": 0.65,      # 🔥 lower
            "PASTE": 0.85,
            "SCROLL_DOWN": 0.85,
            "SCROLL_UP": 0.85,
            "CLOSE": 0.65,     # 🔥 lower
            "NONE": 1.0
        }


        self.last_gesture = "NONE"
        self.stable_count = 0
        self.REQUIRED_FRAMES = 4

        # MediaPipe utils
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = frame.shape

            results = hands.process(rgb)

            # ============================
            # DRAW LANDMARKS
            # ============================
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                        self.mp_draw.DrawingSpec(color=(0, 200, 255), thickness=2)
                    )

            # ============================
            # ML GESTURE PREDICTION
            # ============================
            if not results.multi_hand_landmarks:
                self.last_gesture = "NONE"
                self.stable_count = 0
                self.status_signal.emit("Waiting for hand")
                self.gesture_detected.emit("NONE")
            else:
                lm = results.multi_hand_landmarks[0].landmark

                features = []
                for p in lm:
                    features.extend([p.x, p.y, p.z])

                X = np.array(features).reshape(1, -1)
                X_scaled = self.scaler.transform(X)

                probs = self.model.predict_proba(X_scaled)[0]
                idx = np.argmax(probs)
                gesture = self.model.classes_[idx]
                confidence = probs[idx]

                threshold = self.THRESHOLDS.get(gesture, 0.85)

                self.status_signal.emit(f"{gesture} | conf={confidence:.2f}")

                if gesture == self.last_gesture and confidence >= threshold:
                    self.stable_count += 1
                else:
                    self.last_gesture = gesture
                    self.stable_count = 1

                if self.stable_count >= self.REQUIRED_FRAMES:
                    self.gesture_detected.emit(gesture)
                    self.stable_count = 0
                    self.last_gesture = "NONE"
                else:
                    self.gesture_detected.emit("NONE")

            # ============================
            # SEND FRAME TO UI
            # ============================
            rgb_out = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qimg = QImage(
                rgb_out.data,
                rgb_out.shape[1],
                rgb_out.shape[0],
                QImage.Format.Format_RGB888
            )
            self.frame_signal.emit(qimg)

        cap.release()
        hands.close()

    def stop(self):
        self.running = False
