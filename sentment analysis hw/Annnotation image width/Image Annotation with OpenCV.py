import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)

drawing = False
ix, iy = -1, -1
mode = "pen"

shapes = []

def mouse_draw(event, x, y, flags, param):
    global ix, iy, drawing, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        if mode == "pen":
            shapes.append(("pen", [(x, y)]))

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        if mode == "pen":
            shapes[-1][1].append((x,y))
        else:
            frame_copy =  frame.copy()
            draw_preview(frame_copy, ix, iy, x, y)
    
    elif  event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode != "pen":
            shapes.append((mode, ix, iy, x, y))

def draw_preview(img, x1, y1, x2, y2):
    if mode == "rect":
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
    elif mode == "line":
        cv2.line(img, (x1, y1), (x2, y2), (255,0,0), 2)
    elif mode == "circle":
        r = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
        cv2.circle(img, (x1,y1), r, (0,0,255), 2)

cv2.namedWindow("Live Draw")
cv2.setMouseCallback("Live Draw", mouse_draw)

while True:
    ret,frame = cap.read()
    if not ret:
        break

    frame_copy = frame.copy()

    for item in shapes:
        if item[0] == "pen":
            for i in range(1, len(item[1])):
                cv2.line(frame_copy, item[1][i-1], item[1][i], (0,255,255), 2)
        else:
            m, x1, y1, x2, y2 = item
            if m == "rect":
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0,255,0), 2)
            elif m == "line":
                cv2.line(frame_copy, (x1, y1), (x2, y2), (255,0,0), 2)
            elif m == "circle":
                r = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
                cv2.circle(frame_copy, (x1,y1), r, (0,0,255), 2)

    cv2.putText(frame_copy, f"Mode: {mode.upper()}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
    
    cv2.imshow("Live Draw", frame_copy)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('p'):
        mode = "pen"
    elif key == ord('r'):
        mode = "rect"
    elif key == ord('l'):
        mode = "line"
    elif key == ord('c'):
        mode = "circle"
    elif key == ord('u') and shapes:
        shapes.pop()
    elif key == ord('s'):
        filename = datetime.now().strftime("draw_%Y%m%d_%H%M%S.jpg")
        cv2.imwrite(filename, frame_copy)
        print("Saved:", filename)
        shapes.clear()
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()