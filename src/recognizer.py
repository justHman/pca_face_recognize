import cv2
import numpy as np
from datetime import datetime
import pandas as pd 
import os

MODEL_FILE = r'models\ml\pca_model.npz'
WIDTH = 224
HEIGHT = 224
RECOGNITION_THRESHOLD = 0.24

class Recognizer:
    def __init__(self):
        self.model = None
        self.label_id_to_name = None
        self.load_model()

    def load_model(self):
        data = np.load(MODEL_FILE, allow_pickle=True)
        self.model = {
            'mean': data['mean'],
            'eigenvectors': data['eigenvectors'],
            'projected_data': data['projected_data'],
            'labels': data['labels'],
            'maps': data['maps']
        }
        print("Model PCA đã được tải thành công.")

    def recognize(self, face_image):
        face = cv2.medianBlur(face_image, 3)
        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face_gray = cv2.equalizeHist(face_gray)
        face_resized = cv2.resize(face_gray, (WIDTH, HEIGHT), cv2.INTER_AREA)
        face_flattened = face_resized.flatten().astype(np.float32)

        projected_face = self.model['eigenvectors'] @ (face_flattened - self.model['mean'].flatten())
        
        min_dist = float('inf')
        match_label = -1

        for i, trained_face in enumerate(self.model['projected_data']):
            cos_sim = np.dot(projected_face, trained_face) / (
                np.linalg.norm(projected_face) * np.linalg.norm(trained_face) + 1e-8
            )
            dist = 1 - cos_sim
            if dist < min_dist:
                min_dist = dist
                match_label = self.model['labels'][i]
        
        if min_dist < RECOGNITION_THRESHOLD:
            in4 = self.model['maps'][match_label]
            id, name = in4.split('-')
            return id, name, min_dist
        else:
            return None, "Unknown", min_dist
        

if __name__ == '__main__':
    from face_detector import detect_faces, crop_face
    from attendance_checker import check_attended
    
    recognizer = Recognizer()
    
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)

    attended_list, time_maps = [], {}

    csv_path = "attendance.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        attended_list.extend(df['id'])
        for id, time in zip(df['id'], df['attended_at']):
            time_maps[id] = time
    else:
        df = pd.DataFrame(columns=["id", "name", "attended_at"])

    prev_id, count = None, 0

    while True:
        ret, frame = cap.read()
        faces_coords = detect_faces(frame)

        for (x, y, w, h) in faces_coords:  
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)

            face_img = crop_face(frame, (x, y, w, h))
            id, name, distance = recognizer.recognize(face_img)
            
            color = (0, 255, 0) if id != None else (0, 0, 255) 
            text = f"{id}-{name}"
            if distance is not None:
                text += f" ({distance:.2f})"
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        if len(faces_coords) == 1:
            count, prev_id, attended_list, time_maps, df = check_attended(
                id, name, 
                fps, frame,
                attended_list, time_maps,
                csv_path, df,
                prev_id, count,
                color, 
                x, y, w, h
            )
            
        cv2.imshow("Nhan dang khuon mat - Nhan 'q' de thoat", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()