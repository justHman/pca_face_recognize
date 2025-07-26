"""
🎭 Face Recognition System - Launcher & Demo
=====================================

Khởi động và test toàn bộ hệ thống nhận diện khuôn mặt
Bao gồm: Desktop GUI, Web Interface, Console Mode
"""

import os
import sys
import subprocess
import time
import webbrowser
from datetime import datetime

def print_header():
    print("=" * 60)
    print("🎭 FACE RECOGNITION SYSTEM - LAUNCHER")
    print("=" * 60)
    print("Công nghệ: OpenCV + PCA + Haar Cascade")
    print("Phiên bản: 2025.1")
    print("Thời gian:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

def check_requirements():
    """Kiểm tra các file cần thiết"""
    required_files = [
        "main.py",
        "modern_gui.py", 
        "modern_web_ui.html",
        "web_socket.py",
        "models/ml/pca_model.npz",
        "models/ml/haarcascade_frontalface_default.xml"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Thiếu các file cần thiết:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Tất cả file cần thiết đã sẵn sàng")
    return True

def start_web_server():
    """Khởi động web server"""
    try:
        print("🚀 Đang khởi động Web Socket Server...")
        process = subprocess.Popen([sys.executable, "web_socket.py"], 
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(3)  # Đợi server khởi động
        print("✅ Web Socket Server đã sẵn sàng trên http://localhost:5000")
        return process
    except Exception as e:
        print(f"❌ Lỗi khởi động server: {e}")
        return None

def open_web_interface():
    """Mở giao diện web"""
    try:
        web_path = os.path.abspath("modern_web_ui.html")
        webbrowser.open(f"file:///{web_path}")
        print("🌐 Đã mở giao diện Web trong browser")
        return True
    except Exception as e:
        print(f"❌ Không thể mở browser: {e}")
        return False

def start_desktop_gui():
    """Khởi động giao diện desktop"""
    try:
        print("🖥️ Đang khởi động Desktop GUI...")
        subprocess.Popen([sys.executable, "modern_gui.py"], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("✅ Desktop GUI đã khởi động")
        return True
    except Exception as e:
        print(f"❌ Lỗi khởi động Desktop GUI: {e}")
        return False

def start_console_mode():
    """Khởi động chế độ console"""
    try:
        print("💻 Đang khởi động Console Mode...")
        subprocess.Popen([sys.executable, "main.py"], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("✅ Console Mode đã khởi động")
        return True
    except Exception as e:
        print(f"❌ Lỗi khởi động Console: {e}")
        return False

def show_menu():
    """Hiển thị menu lựa chọn"""
    print("\n🎯 CHỌN CHỨC NĂNG:")
    print("1. 🚀 Khởi động Full System (Web + Desktop)")
    print("2. 🌐 Chỉ Web Interface")
    print("3. 🖥️ Chỉ Desktop GUI")
    print("4. 💻 Chỉ Console Mode")
    print("5. 📊 Demo & Test tất cả")
    print("6. ❌ Thoát")
    
    return input("\nNhập lựa chọn (1-6): ").strip()

def demo_full_system():
    """Demo toàn bộ hệ thống"""
    print("\n🎬 DEMO FULL SYSTEM")
    print("=" * 40)
    
    # Khởi động web server
    server_process = start_web_server()
    if not server_process:
        print("❌ Không thể khởi động server")
        return
    
    # Mở web interface
    time.sleep(1)
    open_web_interface()
    
    # Khởi động desktop GUI
    time.sleep(1)
    start_desktop_gui()
    
    # Khởi động console
    time.sleep(1)
    start_console_mode()
    
    print("\n🎉 DEMO HOÀN TẤT!")
    print("=" * 40)
    print("✅ Web Interface: Mở trong browser")
    print("✅ Desktop GUI: Cửa sổ riêng biệt")
    print("✅ Console Mode: Terminal riêng biệt")
    print("✅ Web Server: Chạy nền")
    
    print("\n📋 HƯỚNG DẪN TEST:")
    print("1. Web Interface: Bật camera → Nhận diện/Điểm danh")
    print("2. Desktop GUI: Real-time processing với UI hiện đại")
    print("3. Console Mode: Xem log chi tiết")
    print("4. Thu thập dữ liệu: SE123456-TenSinhVien")
    
    input("\nNhấn Enter để tiếp tục...")

def show_system_info():
    """Hiển thị thông tin hệ thống"""
    print("\n📋 THÔNG TIN HỆ THỐNG:")
    print("=" * 40)
    print("🔧 Components:")
    print("   - Face Detection: Haar Cascade")
    print("   - Recognition: PCA Algorithm")
    print("   - Web Server: Flask-SocketIO")
    print("   - Desktop GUI: Tkinter Modern")
    print("   - Database: CSV Files")
    
    print("\n🌐 Web Features:")
    print("   - Real-time camera processing")
    print("   - Attendance tracking")
    print("   - Data collection")
    print("   - Export to Excel")
    print("   - Modern responsive UI")
    
    print("\n🖥️ Desktop Features:")
    print("   - Advanced GUI với TTK")
    print("   - System monitoring")
    print("   - Progress indicators")
    print("   - Error handling")
    
    print("\n💻 Console Features:")
    print("   - Direct OpenCV windows")
    print("   - Command line interface")
    print("   - Detailed logging")
    
    print("\n📁 Data Structure:")
    print("   - Images: data/images/ml/")
    print("   - Models: models/ml/")
    print("   - Attendance: attendance.csv")

def main():
    """Hàm chính"""
    print_header()
    
    # Kiểm tra requirements
    if not check_requirements():
        input("\nNhấn Enter để thoát...")
        return
    
    show_system_info()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Full System
            print("\n🚀 KHỞI ĐỘNG FULL SYSTEM")
            server_process = start_web_server()
            if server_process:
                open_web_interface()
                start_desktop_gui()
                print("\n✅ Full System đã sẵn sàng!")
                print("🌐 Web: file:///modern_web_ui.html")
                print("🖥️ Desktop: Cửa sổ GUI riêng")
            
        elif choice == "2":
            # Web Only
            print("\n🌐 KHỞI ĐỘNG WEB INTERFACE")
            server_process = start_web_server()
            if server_process:
                open_web_interface()
                print("✅ Web Interface sẵn sàng!")
            
        elif choice == "3":
            # Desktop Only
            print("\n🖥️ KHỞI ĐỘNG DESKTOP GUI")
            start_desktop_gui()
            
        elif choice == "4":
            # Console Only
            print("\n💻 KHỞI ĐỘNG CONSOLE MODE")
            start_console_mode()
            
        elif choice == "5":
            # Demo
            demo_full_system()
            
        elif choice == "6":
            print("\n👋 Tạm biệt!")
            break
            
        else:
            print("❌ Lựa chọn không hợp lệ!")
        
        input("\nNhấn Enter để quay lại menu...")

if __name__ == "__main__":
    main()
