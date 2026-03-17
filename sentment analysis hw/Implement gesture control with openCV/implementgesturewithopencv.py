import cv2
import numpy as np
import time


def apply_effect(frame, mode, mirror, zoom, brightness, contrast):
    h, w = frame.shape[:2]
    output = frame.copy()

    # Brightness & Contrast
    output = cv2.convertScaleAbs(output, alpha=contrast, beta=brightness)

    if mode == "negative":
        output = cv2.bitwise_not(output)

    elif mode == "blur":
        output = cv2.GaussianBlur(output, (25, 25), 0)

    elif mode == "pixel":
        small = cv2.resize(output, (w//20, h//20))
        output = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    elif mode == "emboss":
        kernel = np.array([
            [-2,-1,0],
            [-1,1,1],
            [0,1,2]
        ])
        output = cv2.filter2D(output, -1, kernel) + 128

    elif mode == "threshold":
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray,120,255,cv2.THRESH_BINARY)
        output = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)

    elif mode == "thermal":
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        output = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    elif mode == "edge":
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,100,200)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif mode == "sketch":
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        inv = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(inv,(21,21),0)
        inv_blur = cv2.bitwise_not(blur)
        sketch = cv2.divide(gray,inv_blur,scale=256.0)
        output = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    elif mode == "cartoon":
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray,7)
        edges = cv2.adaptiveThreshold(gray,255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY,9,9)
        color = cv2.bilateralFilter(output,9,300,300)
        output = cv2.bitwise_and(color,color,mask=edges)

    elif mode == "sharpen":
        kernel = np.array([
            [0,-1,0],
            [-1,5,-1],
            [0,-1,0]
        ])
        output = cv2.filter2D(output,-1,kernel)

    if mirror:
        output = cv2.flip(output,1)

    if zoom:
        cx, cy = w//2, h//2
        crop = output[cy-120:cy+120, cx-160:cx+160]
        output = cv2.resize(crop,(w,h))

    return output


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera failed")
        return

    mode = None
    mirror = False
    zoom = False
    brightness = 0
    contrast = 1.0

    prev_time = 0

    print("""
Controls
--------------------------------
n = Negative
b = Blur
x = Pixel
e = Emboss
t = Threshold
m = Thermal
g = Edge Detection
k = Sketch
c = Cartoon
h = Sharpen

r = Mirror Toggle
z = Zoom Toggle

+ = Increase Brightness
- = Decrease Brightness

s = Screenshot
o = Original
q = Quit
--------------------------------
""")

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        output = apply_effect(frame, mode, mirror, zoom, brightness, contrast)

        # FPS
        current = time.time()
        fps = 1/(current-prev_time) if prev_time!=0 else 0
        prev_time = current

        cv2.putText(output,f"FPS: {int(fps)}",(10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.imshow("Advanced Visual Effects Lab", output)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('n'):
            mode="negative"
        elif key == ord('b'):
            mode="blur"
        elif key == ord('x'):
            mode="pixel"
        elif key == ord('e'):
            mode="emboss"
        elif key == ord('t'):
            mode="threshold"
        elif key == ord('m'):
            mode="thermal"
        elif key == ord('g'):
            mode="edge"
        elif key == ord('k'):
            mode="sketch"
        elif key == ord('c'):
            mode="cartoon"
        elif key == ord('h'):
            mode="sharpen"

        elif key == ord('r'):
            mirror = not mirror
        elif key == ord('z'):
            zoom = not zoom

        elif key == ord('+'):
            brightness += 10
        elif key == ord('-'):
            brightness -= 10

        elif key == ord('s'):
            cv2.imwrite("screenshot.png", output)
            print("Screenshot saved!")

        elif key == ord('o'):
            mode=None
            mirror=False
            zoom=False

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()