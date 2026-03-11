import cv2
import time

def load_face_detector():
    return cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

def initialize_camera(camera_index=0):
    return cv2.VideoCapture(camera_index)

def preprocess_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def detect_faces(detector, gray_frame):
    return detector.detectMultiScale(
        gray_frame,
        scaleFactor=1.3,
        minNeighbors=5
    )

def draw_faces(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        # draw center point
        cx = x + w // 2
        cy = y + h // 2
        cv2.circle(frame, (cx, cy), 4, (255,0,0), -1)

    return frame

def display_info(frame, face_count, fps):
    cv2.putText(frame, f"Faces: {face_count}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (10,70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

def run_face_detection():
    detector = load_face_detector()
    camera = initialize_camera()

    prev_time = 0
    gray_mode = False
    img_count = 0

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        gray = preprocess_frame(frame)
        faces = detect_faces(detector, gray)

        frame = draw_faces(frame, faces)

        # FPS calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        display_info(frame, len(faces), fps)

        # grayscale toggle
        if gray_mode:
            frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        cv2.imshow("Advanced Face Detection", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite(f"screenshot_{img_count}.png", frame)
            print("Screenshot saved!")
            img_count += 1
        elif key == ord("g"):
            gray_mode = not gray_mode

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_face_detection()