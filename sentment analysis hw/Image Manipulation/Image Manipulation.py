import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
brightness = 0
contrast = 1.0
blur = 0
is_gray = False
rotation_angle = 0
flip_mode = None
edge_mode = False

zoom= 1.0
prev_time=0
def draw_ui(img, fps):
    panel = img.copy()
    cv2.putText(panel, f"FPS: {int(fps)}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    y = 55
    Controls = [
        "Q - Quit",
        "G - Grayscale",
        "B/N - Brightness +/-",
        "C/V - Contrast +/-",
        "L/R - Rotate",
        "H - Flip Horizontal",
        "E - Edge Detection", -
        "U/J - Zoom +/-",
        "K/M - Blur +/-",
        "S - Save Snapshot",
        "X - Reset"
    ]
    for t in Controls:
        cv2.putText(panel, t, (10, y),  cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 1)
        y += 22
    return panel

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    img = frame.copy()

    if zoom != 1:
        nh,  nw = int(h / zoom), int(w / zoom)
        y1 = (h - nh) // 2
        x1 = (w - nw) // 2
        crop = img[y1:y1+nh, x1:x1+nw]
        img = cv2.resize(crop, (w, h))

    if is_gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

    if blur > 0:
        img = cv2.GaussianBlur(img, (blur*2+1, blur*2+1), 0)

    if edge_mode:
        edges = cv2.Canny(img, 800, 150)
        img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if rotation_angle != 0:
        matrix = cv2.getRotationMatrix2D((w//2, h//2), rotation_angle, 1)
        img = cv2.warpAffine(img, matrix, (w, h))

    if flip_mode is not None:
        img = cv2.flip(img, flip_mode)

    current_time = time.time
    fps = 1/ (current_time - prev_time) if prev_time!= 0 else 0
    prev_time = current_time

    img = draw_ui(img, fps)

    cv2.imshow("Advanced Image Manipulation System", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('g'):
        is_gray = not is_gray
    elif key == ord('b'):
        brightness += 10
    elif key == ord('n'): 
        brightness -= 10
    elif key == ord('c'): 
        contrast += 0.1
    elif key == ord('v'): 
        contrast = 0.1
    elif key == ord('1'): 
        rotation_angle -= 90
    elif key == ord('r'):
        rotation_angle += 90
    elif key == ord('h'):
        flip_mode = None if flip_mode == 1 else 1
    elif key == ord('e'):
        edge_mode = not edge_mode
    elif key == ord('u'): 
        zoom + 0.1
    elif key == ord('j'):
        zoom = 0.1
        zoom = max(1.0, zoom)
    elif key == ord('k'):
        blur += 1
    elif key == ord('m'):
        blur = max(0, blur - 1)
    elif key == ord('s'):
        cv2.imwrite(f"snapshot_{int(time.time())}.png", img)
    elif key == ord('x'):
        brightness = 0
        contrast = 1.0
        blur = 0
        is_gray = False
        rotation_angle = 0
        flip_mode = None
        edge_mode = False
        zoom = 1.0
cap.release()
cv2.destroyAllWindows()