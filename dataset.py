import cv2
import mediapipe as mp
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

label = int(input("Enter label (0-3): "))

with open('data.csv', 'a', newline='') as f:
    writer = csv.writer(f)

    while True:
        ret, frame = cap.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lm_list = []
                for lm in handLms.landmark:
                    lm_list.append(lm.x)
                    lm_list.append(lm.y)

                writer.writerow(lm_list + [label])

        cv2.imshow("Dataset", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()