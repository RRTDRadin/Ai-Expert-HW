import cv2
import numpy as np

cap = cv2.VideoCapture(0)

brightness = 0
is_gray = False
rotation_angle = 0
flip_mode = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img = frame.copy()

    if is_gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    img = cv2.convertScaleAbs(img, alpha=1, beta=brightness)

    if rotation_angle != 0:
        h, w= img.shape[:2]
        matrix = cv2.getRotationMatrix2D((w // 2, h // 2), rotation_angle, 1)
        img =  cv2.warpAffine(img, matrix, (w,h))

    if flip_mode is not None:
        img = cv2.flip(img, flip_mode)

    cv2.imshow("Image Manipulation System", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('g'):
        is_gray = not is_gray
    elif key == ord('b'):
        brightness += 10
    elif key == ord('n'):
        brightness -= 10
    elif key == ord('l'):
        rotation_angle -= 90
    elif key == ord('r'):
        rotation_angle += 90
    elif key == ord('h'):
        flip_mode = None  if flip_mode == 1 else 1

cap.release()
cv2.destroyAllWindows()
