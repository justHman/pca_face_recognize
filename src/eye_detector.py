import cv2
import os

# Đường dẫn đến file haarcascade nhận diện mắt
EYE_CASCADE_PATH = r'venv\Lib\site-packages\cv2\data\haarcascade_eye_tree_eyeglasses.xml'

eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_PATH)

def detect_eyes(image):
    """
    Trả về danh sách các bounding box của mắt trong ảnh.
    Mỗi bounding box là tuple (x, y, w, h).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20)
    )
    return eyes

if __name__ == "__main__":
    # Test nhanh với webcam
    count_eye = 0
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        eyes = detect_eyes(frame)
        if len(eyes) == 0:
            print(f'Bạn đã chớm mắt {count_eye+ + 1} lần.')
            count_eye += 1

        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.imshow("Eye Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()