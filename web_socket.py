import eventlet
eventlet.monkey_patch()

import cv2
import numpy as np
import base64
import os
import pandas as pd
from datetime import datetime
from flask import Flask, request, render_template_string
from flask_socketio import SocketIO, emit
from src.face_detector import detect_faces, crop_face
from src.recognizer import Recognizer
from src.data_collector import DataCollector

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

try:
    recognizer = Recognizer()
    data_collector = DataCollector()
except:
    recognizer = None
    data_collector = None
    print("Warning: Could not load recognizer model or data collector")

client_states = {}

@app.route('/')
def index():
    with open('web_ui.html', 'r', encoding='utf-8') as f:
        return f.read()

@socketio.on('frame')
def handle_frame(data):
    if not recognizer:
        emit('result', {'error': 'Model not loaded'})
        return
        
    sid = request.sid
    img_str = data['image'].split(',')[-1]
    img_bytes = base64.b64decode(img_str)
    npimg = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if image is None:
        emit('result', {'error': 'Cannot decode image'})
        return

    faces_coords = detect_faces(image)
    # Chỉ xử lý khi có đúng 1 khuôn mặt
    if len(faces_coords) == 1:
        (x, y, w, h) = faces_coords[0]
        face_img = crop_face(image, (x, y, w, h))
        id, name, distance = recognizer.recognize(face_img)

        # Lấy trạng thái cũ hoặc khởi tạo mới
        state = client_states.get(sid, {"prev_id": None, "count": 0})

        if id is not None:
            if state["prev_id"] and state["prev_id"] == id:
                state["count"] += 1
                # Đủ 60 frame liên tục cùng 1 id
                if state["count"] >= 60:
                    # Save attendance
                    save_attendance(id, name)
                    emit('result', {"id": id, "name": name, "distance": float(distance)})
                    state["count"] = 0  # Reset sau khi trả về
                else:
                    emit('result', {"name": name, "progress": state["count"], "distance": float(distance)})
            else:
                state["count"] = 1
                state["prev_id"] = id
                emit('result', {"name": name, "progress": 1, "distance": float(distance)})
        else:
            state["count"] = 0
            state["prev_id"] = None
            emit('result', {"name": name, "distance": float(distance)})

        client_states[sid] = state
    else:
        emit('result', {'error': f'Detected {len(faces_coords)} faces, need exactly 1'})

def save_attendance(id, name):
    """Save attendance to CSV file"""
    csv_path = "attendance.csv"
    current_time = str(datetime.now())[:-7]
    
    # Check if file exists
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        # Check if already attended today
        today = datetime.now().date()
        existing = df[df['id'] == id]
        if not existing.empty:
            last_attendance = pd.to_datetime(existing.iloc[-1]['attended_at']).date()
            if last_attendance == today:
                return  # Already attended today
        
        # Add new record
        new_data = {"id": id, "name": name, "attended_at": current_time}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(csv_path, index=False)
    else:
        # Create new file
        df = pd.DataFrame([{"id": id, "name": name, "attended_at": current_time}])
        df.to_csv(csv_path, index=False)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in client_states:
        del client_states[sid]

@socketio.on('start_data_collection')
def handle_start_data_collection(data):
    if not data_collector:
        emit('collection_error', {'error': 'Data collector not available'})
        return
        
    student_info = data.get('studentInfo', '')
    if not student_info or '-' not in student_info:
        emit('collection_error', {'error': 'Invalid student info format'})
        return
    
    sid = request.sid
    client_states[sid] = {
        "mode": "data_collection",
        "student_info": student_info,
        "count": 0,
        "target": 20
    }
    emit('collection_started', {'studentInfo': student_info, 'target': 20})

@socketio.on('collection_frame')
def handle_collection_frame(data):
    sid = request.sid
    state = client_states.get(sid, {})
    
    if state.get("mode") != "data_collection":
        emit('collection_error', {'error': 'Not in data collection mode'})
        return
    
    if state.get("count", 0) >= state.get("target", 20):
        emit('collection_complete', {'total': state.get("count", 0)})
        return
    
    img_str = data['image'].split(',')[-1]
    img_bytes = base64.b64decode(img_str)
    npimg = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    if image is None:
        emit('collection_error', {'error': 'Cannot decode image'})
        return

    faces_coords = detect_faces(image)
    if len(faces_coords) == 1:
        (x, y, w, h) = faces_coords[0]
        face_img = crop_face(image, (x, y, w, h))
        
        student_info = state.get("student_info", "")
        try:
            success = data_collector.save_face_image(face_img, student_info, state.get("count", 0) + 1)
            if success:
                state["count"] += 1
                client_states[sid] = state
                emit('collection_progress', {
                    'current': state["count"], 
                    'target': state.get("target", 20),
                    'percentage': (state["count"] / state.get("target", 20)) * 100
                })
                
                if state["count"] >= state.get("target", 20):
                    emit('collection_complete', {'total': state["count"]})
            else:
                emit('collection_error', {'error': 'Failed to save image'})
        except Exception as e:
            emit('collection_error', {'error': str(e)})
    else:
        emit('collection_error', {'error': f'Need exactly 1 face, detected {len(faces_coords)}'})

if __name__ == "__main__":
    socketio.run(app, port=5000)