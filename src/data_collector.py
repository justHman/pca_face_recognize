import cv2
import os
from .face_detector import crop_face, detect_faces
import time

WIDTH = 224
HEIGHT = 224
DATASET_PATH = r'data\images\ml'

def save_face_data(frame, bboxs, in4):
    if len(bboxs) == 0:
        print("[LỖI] Không tìm thấy khuôn mặt nào để lưu.")
        return False
    
    bbox = max(bboxs, key=lambda f: f[2]*f[3])
  
    face = crop_face(frame, bbox)
    
    face = cv2.medianBlur(face, 3)
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.equalizeHist(face)
    face = cv2.resize(face, (WIDTH, HEIGHT))
    
    id, name = in4.split('-')
    name_folder = os.path.join(DATASET_PATH, in4)
    os.makedirs(name_folder, exist_ok=True)

    len_files = len(os.listdir(name_folder))
    file_path = os.path.join(name_folder, f"{name}_{len_files + 1}.jpg")
    
    cv2.imwrite(file_path, face)
    print(f"Đã lưu ảnh vào: {file_path}")

    return True

if __name__ == "__main__":
    in4 = input("Enter ur in4 (SE123456-Nam): ")
    if not in4:
        print("Tên không được để trống. Vui lòng chạy lại.")
        exit()

    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        print("Lỗi: Không thể mở camera.")
        exit()

    frame_indx, count = 0, 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Lỗi: Không thể đọc frame từ camera.")
            break

        faces = detect_faces(frame)

        display_frame = frame.copy() 
        for (x, y, w, h) in faces:
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(display_frame, 'Face Detected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow(f"Thu thap du lieu cho '{in4}' - Nhan 's' de luu, 'q' de thoat", display_frame)
      
        if frame_indx == 0:
            time.sleep(2)

        if len(faces) == 1 and frame_indx % 10 == 0:
            save_face_data(frame, faces, in4)
            count += 1
            if count == 20:
                break
            
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            save_face_data(frame, faces, in4)

        frame_indx += 1

    cap.release()
    cv2.destroyAllWindows()

class DataCollector:
    def __init__(self):
        self.dataset_path = DATASET_PATH
        
    def save_face_image(self, face_img, student_info, index):
        """Save face image for web interface"""
        try:
            # Create directory if not exists
            person_dir = os.path.join(self.dataset_path, student_info)
            if not os.path.exists(person_dir):
                os.makedirs(person_dir)
            
            # Resize face image
            face_resized = cv2.resize(face_img, (WIDTH, HEIGHT))
            
            # Save image
            filename = f"{student_info}_{index}.jpg"
            filepath = os.path.join(person_dir, filename)
            cv2.imwrite(filepath, face_resized)
            
            print(f"Saved: {filepath}")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False