import cv2
import os
from face_detector import crop_face, detect_faces

WIDTH = 224
HEIGHT = 224
DATASET_PATH = r'data\images\ml'

def save_face_data(frame, bboxs, in4):
    if len(bboxs) == 0:
        print("[LỖI] Không tìm thấy khuôn mặt nào để lưu.")
        return False
    
    bbox = max(bboxs, key=lambda f: f[2]*f[3])
  
    face = crop_face(frame, bbox)
    
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
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

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            save_face_data(frame, faces, in4)
      
    cap.release()
    cv2.destroyAllWindows()