import cv2
import pandas as pd
from datetime import datetime

def check_attended(
        id, name, 
        fps, frame, 
        attended_list, time_maps, 
        csv_path, df,
        prev_id, count,
        color,
        x, y, w, h
    ):
    if id != None:
        if prev_id and prev_id == id and id not in attended_list:
            count += 1
            if count == fps * 2:
                attended_list.append(id)
                time_maps[id] = str(datetime.now())[:-7]
                new_data = {"id": id, "name": name, "attended_at": time_maps[id]}

                if id not in df['id']:
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
        count = 0
    return count, prev_id, attended_list, time_maps, df