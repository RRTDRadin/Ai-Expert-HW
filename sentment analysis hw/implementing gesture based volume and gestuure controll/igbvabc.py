import cv2
import numpy as np
import math
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# Camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(detectionCon=0.8, maxHands=1)

# Screen size
screen_w, screen_h = pyautogui.size()

# Smoothening
prev_x, prev_y = 0, 0
smoothening = 7

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        if len(lmList) >= 9:
            x1, y1 = lmList[8][0], lmList[8][1]  # Index finger
            x2, y2 = lmList[12][0], lmList[12][1]  # Middle finger

            # Convert to screen coordinates
            screen_x = np.interp(x1, [0, 640], [0, screen_w])
            screen_y = np.interp(y1, [0, 480], [0, screen_h])

            # Smooth movement
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            # Draw pointer
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), -1)

            # Distance for click
            length = math.hypot(x2 - x1, y2 - y1)

            # LEFT CLICK (pinch)
            if length < 30:
                cv2.putText(img, "LEFT CLICK", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                pyautogui.click()

    cv2.imshow("Hand Mouse Controller", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()