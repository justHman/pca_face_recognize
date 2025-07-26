# 🎭 Hệ thống Nhận diện Khuôn mặt & Điểm danh

Hệ thống nhận diện khuôn mặt tự động sử dụng PCA (Principal Component Analysis) và OpenCV với giao diện người dùng hiện đại.

## ✨ Tính năng chính

- 📸 **Thu thập dữ liệu**: Tự động chụp và lưu ảnh khuôn mặt
- 🤖 **Huấn luyện model**: Sử dụng PCA để tạo model nhận diện
- 👥 **Nhận diện khuôn mặt**: Nhận diện real-time qua webcam
- 📋 **Điểm danh tự động**: Tự động ghi nhận điểm danh vào CSV
- 🖥️ **Giao diện đa dạng**: Desktop GUI (Tkinter) và Web UI
- 📊 **Xuất báo cáo**: Xuất dữ liệu ra Excel/CSV

## 🏗️ Cấu trúc project

```
face_recognize/
├── 🎯 main.py                 # Chương trình chính (OpenCV)
├── 🖥️ gui_main.py            # Giao diện desktop (Tkinter)
├── 🌐 web_socket_new.py      # Server web (Flask-SocketIO)
├── 🌐 web_ui.html            # Giao diện web hiện đại
├── 📄 attendance.csv         # Dữ liệu điểm danh
├── 📋 requirements.txt       # Dependencies
├── src/
│   ├── 📸 data_collector.py  # Thu thập dữ liệu
│   ├── 👁️ face_detector.py   # Phát hiện khuôn mặt (Haar Cascade)
│   ├── 🧠 recognizer.py      # Nhận diện khuôn mặt (PCA)
│   ├── 🎓 trainer.py         # Huấn luyện model
│   └── 📊 attendance_checker.py
├── data/images/ml/           # Dữ liệu ảnh khuôn mặt
├── models/ml/                # Model đã huấn luyện
└── utils/                    # Tiện ích
```

## 🚀 Hướng dẫn cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Tạo thư mục cần thiết

```bash
mkdir data\images\ml
mkdir models\ml
mkdir temp
```

### 3. Download Haar Cascade model

Tải file `haarcascade_frontalface_default.xml` từ OpenCV và đặt vào `models/ml/`

## 📱 Các cách sử dụng

### 🖥️ Giao diện Desktop (Tkinter)

```bash
python gui_main.py
```

**Tính năng:**
- ✅ Giao diện thân thiện, dễ sử dụng
- ✅ Hiển thị camera real-time
- ✅ Thu thập dữ liệu, huấn luyện model
- ✅ Điểm danh với progress bar
- ✅ Bảng dữ liệu điểm danh
- ✅ Xuất Excel

### 🌐 Giao diện Web

```bash
python web_socket_new.py
```

Mở trình duyệt: `http://localhost:5000`

**Tính năng:**
- ✅ Giao diện web hiện đại, responsive
- ✅ Real-time WebSocket communication
- ✅ Thống kê điểm danh
- ✅ Nhật ký hệ thống
- ✅ Notification đẹp mắt

### 💻 Terminal/Console (OpenCV)

```bash
python main.py
```

**Tính năng:**
- ✅ Chạy trực tiếp, không cần GUI
- ✅ Hiệu suất cao
- ✅ Phù hợp demo nhanh

## 📖 Hướng dẫn sử dụng chi tiết

### Bước 1: Thu thập dữ liệu

1. **Desktop**: Click "Thu thập dữ liệu", nhập thông tin theo format `SE123456-TenSinhVien`
2. **Web**: Nhập thông tin và click "📸 Thu thập"
3. **Console**: Chạy `python src/data_collector.py`

Hệ thống sẽ tự động chụp 20 ảnh khuôn mặt và lưu vào thư mục tương ứng.

### Bước 2: Huấn luyện Model

```bash
python src/trainer.py
```

Hoặc click nút "Huấn luyện Model" trong GUI.

### Bước 3: Điểm danh

1. Bật camera
2. Click "Điểm danh" 
3. Hệ thống sẽ nhận diện và tự động ghi nhận sau 2 giây

## 🎯 API Endpoints

### REST API

```bash
python api.py
```

- `POST /recognize`: Upload ảnh để nhận diện

### WebSocket API

- `frame`: Gửi frame ảnh để nhận diện
- `result`: Nhận kết quả nhận diện

## 📊 Thuật toán sử dụng

### 1. Phát hiện khuôn mặt: **Haar Cascade**
- ✅ Nhanh, nhẹ
- ✅ Phù hợp real-time
- ❌ Độ chính xác trung bình

### 2. Nhận diện khuôn mặt: **PCA (Principal Component Analysis)**
- ✅ Giảm chiều dữ liệu hiệu quả
- ✅ Tốc độ nhanh
- ✅ Phù hợp dataset nhỏ-trung bình
- ❌ Nhạy cảm với ánh sáng và góc chụp

### 3. Tiền xử lý ảnh:
- Median Blur: Giảm noise
- Grayscale: Chuyển ảnh xám  
- Histogram Equalization: Cân bằng sáng
- Resize: Chuẩn hóa kích thước (224x224)

## ⚙️ Cấu hình

### Tham số trong `recognizer.py`:
```python
WIDTH = 224                    # Chiều rộng ảnh
HEIGHT = 224                   # Chiều cao ảnh  
RECOGNITION_THRESHOLD = 0.4    # Ngưỡng nhận diện
```

### Tham số trong `face_detector.py`:
```python
scaleFactor = 1.3              # Tỷ lệ scale
minNeighbors = 5               # Số neighbor tối thiểu
minSize = (30, 30)             # Kích thước khuôn mặt tối thiểu
```

## 🎨 Screenshots

### Desktop GUI
![Desktop GUI](https://via.placeholder.com/600x400?text=Desktop+GUI+Screenshot)

### Web UI  
![Web UI](https://via.placeholder.com/600x400?text=Web+UI+Screenshot)

## 🔧 Troubleshooting

### Lỗi thường gặp:

**1. Không thể mở camera:**
```bash
# Kiểm tra camera có hoạt động không
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

**2. Lỗi model không tồn tại:**
```bash
# Chạy lại training
python src/trainer.py
```

**3. Lỗi Haar Cascade:**
- Download `haarcascade_frontalface_default.xml` từ OpenCV GitHub
- Đặt vào thư mục `models/ml/`

**4. Lỗi dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

## 📈 Cải tiến trong tương lai

- 🔄 **Deep Learning**: Thay PCA bằng CNN/FaceNet
- 🌡️ **Liveness Detection**: Phát hiện ảnh giả, video giả
- 📱 **Mobile App**: Phát triển app di động
- 🏢 **Multi-tenant**: Hỗ trợ nhiều tổ chức
- 📊 **Analytics**: Dashboard thống kê chi tiết
- 🔐 **Security**: Mã hóa dữ liệu, authentication

## 🤝 Đóng góp

1. Fork project
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Liên hệ

- **Author**: [Tên của bạn]
- **Email**: [Email của bạn]
- **Project Link**: [https://github.com/justHman/face_recognize_pca](https://github.com/justHman/face_recognize_pca)

---

⭐ **Nếu project hữu ích, hãy cho một star nhé!** ⭐
