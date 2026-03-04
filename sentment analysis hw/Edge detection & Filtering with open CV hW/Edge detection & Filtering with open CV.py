import cv2
import numpy as np

cap = cv2.VideoCapture(0)

current_mode = 'original'
gaussian_kernel = 9
median_kernel = 9

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output = frame.copy()

    if current_mode == 'laplacian':
        lap = cv2.Laplacian (gray, cv2.CV_64F)
        output = cv2.cvtColor(np.uint8(np.absolute (lap)), cv2.COLOR_GRAY2BGR)

    elif current_mode == 'sobel':
        sx = cv2.Sobel (gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.magnitude (sx, sy)
        output = cv2.cvtColor(np.uint8(np.absolute (sobel)), cv2.COLOR_GRAY2BGR)

    elif current_mode == 'canny':
        edges = cv2.Canny (gray, 80, 160)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif current_mode == 'gaussian':
        if gaussian_kernel % 2 == 0:
            gaussian_kernel += 1
        output = cv2.GaussianBlur (frame, (gaussian_kernel, gaussian_kernel), 2)

    elif current_mode == 'median':
        if median_kernel % 2 == 0:
            median_kernel += 1
        output = cv2.medianBlur (frame, median_kernel)

    cv2.putText(output, f'Mode: (current_mode)', (10, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.imshow("Advanced Edge Detection System", output)

    key= cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('o'):
        current_mode = 'original'
    elif key == ord('l'):
        current_mode = 'laplacian'
    elif key == ord('s'):
        current_mode = 'sobel'
    elif key == ord('c'):
        current_mode = 'canny'
    elif key == ord('g'):
        current_mode = 'gaussian'
    elif key == ord('m'):
        current_mode = 'median'

    elif key == ord('+') and current_mode == 'gaussian':
        gaussian_kernel = min(51, gaussian_kernel + 4)
    elif key == ord('-') and current_mode == 'gaussian':
        gaussian_kernel = max(3, gaussian_kernel - 4)

    elif key == ord(']') and current_mode == 'median':
        median_kernel = min(51, median_kernel + 4)
    elif key == ord('[') and current_mode == 'median':
        median_kernel = max(3, median_kernel - 4)

cap.release()
cv2.destroyAllWindows()