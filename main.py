import cv2
import pandas as pd
from src.face_detector import detect_faces, crop_face
from src.recognizer import Recognizer
from datetime import datetime
import os 

if __name__ == '__main__':
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
            in4, distance = recognizer.recognize(face_img)
            
            color = (0, 255, 0) if in4 != "Unknown" else (0, 0, 255) 
            text = f"{in4}"
            if distance is not None:
                text += f" ({distance:.2f})"
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if in4 != "Unknown":
                id, name = in4.split('-')
                if prev_id and prev_id == id and id not in attended_list:
                    count += 1
                    if count == fps * 2:
                        attended_list.append(id)
                        time_maps[id] = str(datetime.now())[:-7]
                        new_data = {"id": id, "name": name, "attended_at": time_maps[id]}

                        if name not in df['name'].values:
                            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                            df.to_csv(csv_path, index=False)
                    elif count < 60: 
                        cv2.putText(frame, f'{count / fps:.2f}s', (x, y + h + h // 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                else:
                    count = 0
                    prev_id = id

                if id in attended_list:
                    cv2.putText(frame, f'Attended at {time_maps[id]}', (x - w // 2, y + h + h // 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            else:
                continue

        
        cv2.imshow("Nhan dang khuon mat - Nhan 'q' de thoat", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()