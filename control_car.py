import cv2
import mediapipe as mp
import pickle
import serial
import time
from collections import deque

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Serial (CHANGE COM PORT)
ser = serial.Serial('COM3', 9600)
time.sleep(2)

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Eye detection (AUTO LOAD)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

cap = cv2.VideoCapture(0)

# Buffers
prediction_buffer = deque(maxlen=5)
distance_buffer = deque(maxlen=5)

last_command = ''
eye_closed_counter = 0
no_hand_counter = 0

# Send only when changed
def send_command(cmd):
    global last_command
    if cmd != last_command:
        ser.write(cmd.encode())
        last_command = cmd

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ---- EYE DETECTION ----
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    if len(eyes) == 0:
        eye_closed_counter += 1
    else:
        eye_closed_counter = 0

    # ---- SAFETY STOP (EYES) ----
    if eye_closed_counter > 15:
        send_command('S')
        cv2.putText(frame, "STOP - Eyes Closed", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    else:
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
                    send_command('S')
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
                cv2.putText(frame, "STOP - No Hand", (50,90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()