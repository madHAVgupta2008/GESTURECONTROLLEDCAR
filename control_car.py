import cv2
import mediapipe as mp
import pickle
import serial
import time
from collections import deque

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Serial (CHANGE COM PORT)
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

# Buffers
prediction_buffer = deque(maxlen=5)
distance_buffer = deque(maxlen=5)

last_command = ''
no_hand_counter = 0
bluetooth_connected = True

# Send only when changed
def send_command(cmd):
    global last_command, bluetooth_connected
    if cmd != last_command:
        try:
            ser.write(cmd.encode())
            last_command = cmd
            bluetooth_connected = True
        except:
            bluetooth_connected = False

while True:
    ret, frame = cap.read()

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # ---- HAND PRESENT ----
    if results.multi_hand_landmarks:
        no_hand_counter = 0

        for handLms in results.multi_hand_landmarks:
            lm_list = []

            for lm in handLms.landmark:
                lm_list.append(lm.x)
                lm_list.append(lm.y)

            # ---- SPEED CONTROL ----
            wrist = handLms.landmark[0]
            middle_tip = handLms.landmark[12]

            distance = abs(middle_tip.y - wrist.y)
            distance_buffer.append(distance)

            smooth_distance = sum(distance_buffer) / len(distance_buffer)

            if smooth_distance < 0.1:
                send_command('1')
            elif smooth_distance < 0.2:
                send_command('2')
            else:
                send_command('3')

            # ---- GESTURE CONTROL ----
            prediction = model.predict([lm_list])[0]
            prediction_buffer.append(prediction)

            final_prediction = max(set(prediction_buffer),
                                   key=prediction_buffer.count)

            if final_prediction == 0:
                send_command('B')
            elif final_prediction == 1:
                send_command('F')
            elif final_prediction == 2:
                send_command('R')
            elif final_prediction == 3:
                send_command('L')

    # ---- NO HAND DETECTED ----
    else:
        no_hand_counter += 1

        if no_hand_counter > 10:
            send_command('S')
            cv2.putText(frame, "STOP - No Hand", (50, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # ---- BLUETOOTH STATUS DISPLAY ----
    if not bluetooth_connected:
        cv2.putText(frame, "BLUETOOTH DISCONNECTED", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        cv2.putText(frame, "Bluetooth Connected", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()