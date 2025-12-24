import cv2
import csv
import os
import mediapipe as mp

# =========================
# CONFIG
# =========================
GESTURES = [
    "COPY",        # fist
    "PASTE",       # palm
    "SCROLL_DOWN", # peace
    "SCROLL_UP",   # index
    "CLOSE",       # thumbs up
    "NONE"
]

SAVE_PATH = "gesture_data.csv"
SAMPLES_PER_GESTURE = 300

# =========================
# MEDIAPIPE SETUP
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

# =========================
# CSV SETUP
# =========================
file_exists = os.path.isfile(SAVE_PATH)
csv_file = open(SAVE_PATH, "a", newline="")
writer = csv.writer(csv_file)

if not file_exists:
    header = []
    for i in range(21):
        header += [f"x{i}", f"y{i}", f"z{i}"]
    header.append("label")
    writer.writerow(header)

# =========================
# COLLECTION LOOP
# =========================
print("\nGesture list:")
for i, g in enumerate(GESTURES):
    print(f"{i} → {g}")

current_gesture = None
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    cv2.putText(
        frame,
        f"Gesture: {current_gesture}  Count: {count}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    if results.multi_hand_landmarks and current_gesture:
        lm = results.multi_hand_landmarks[0].landmark
        row = []
        for p in lm:
            row.extend([p.x, p.y, p.z])
        row.append(current_gesture)
        writer.writerow(row)
        count += 1

    cv2.imshow("Gesture Data Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press number key to select gesture
    if key in [ord(str(i)) for i in range(len(GESTURES))]:
        current_gesture = GESTURES[int(chr(key))]
        count = 0
        print(f"\nCollecting: {current_gesture}")

    # Auto move to NONE when enough samples
    if count >= SAMPLES_PER_GESTURE:
        print(f"Finished {current_gesture}")
        current_gesture = None
        count = 0

    if key == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()
