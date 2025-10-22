# Face Recognition System with PCA  

A real-time face recognition and attendance system built using OpenCV and Principal Component Analysis (PCA). This system can collect face data, train recognition models, and perform real-time face recognition for attendance tracking.

## Features
 
- 🎥 Real-time face detection and recognition  
- 📊 PCA-based facial recognition model
- 📝 Automatic attendance tracking with CSV export
- 🖼️ Face data collection and management
- 🎯 High accuracy with distance-based confidence scoring
- ⏱️ Time-based attendance confirmation (2-second hold)

## System Requirements

- Python 3.7 or higher
- Webcam/Camera device
- Windows OS (tested on Windows 10/11)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/justHman/face_recognize_pca.git
cd face_recognize_pca
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Automated Setup (Recommended)

For the easiest setup, use the provided batch script that will guide you through the entire process:

1. **Double-click `setup_and_run.bat`** or run it from command prompt
```bash
python setup_and_run.bat
```
3. Follow the on-screen prompts
4. The script will automatically:
   - Set up the Python environment
   - Run data collection
   - Train the model
   - Start the recognition system

### Option 2: Manual Setup

Follow these steps in order:

#### Step 1: Data Collection

First, collect face data for people you want to recognize:

```bash
python src/data_collector.py
```

- Enter person information in format: `ID-Name` (e.g., `SE194190-Nam`)
- Look directly at the camera
- The system will automatically capture 20 face images
- Press 'q' to quit 

#### Step 2: Train the Model

Train the PCA recognition model with collected data:

```bash
python src/trainer.py
```

This will:
- Process all collected face images
- Create a PCA model with 98% variance retention
- Save the model to `models/ml/pca_model.npz`

#### Step 3: Run Recognition System

Start the real-time face recognition:

```bash
python main.py
```

**Or use the standalone recognizer:**

```bash
python src/recognizer.py
```

## Usage Instructions

### Data Collection Mode
1. Run the data collector
2. Enter person ID and name when prompted (format: `ID-Name`)
3. Position your face in front of the camera
4. Wait for automatic capture of 20 images
5. Repeat for additional people

### Recognition Mode
1. The system will start your default camera
2. Face detection is shown with blue rectangles
3. Recognized faces show green rectangles with ID and name
4. Unknown faces show red rectangles
5. For attendance: Hold position for 2 seconds to confirm attendance
6. Press 'q' to quit the application

### Attendance Tracking
- The system automatically tracks attendance in `attendance.csv`
- Each person needs to hold their position for 2 seconds
- Duplicate attendance on the same day is prevented
- Attendance time is recorded with timestamp

## Project Structure

```
face_recognize_pca/
├── data/
│   └── images/
│       └── ml/              # Training face images
├── models/
│   └── ml/
│       ├── haarcascade_frontalface_default.xml
│       └── pca_model.npz    # Trained PCA model
├── src/
│   ├── attendance_checker.py
│   ├── data_collector.py    # Face data collection
│   ├── face_detector.py     # Face detection utilities
│   ├── recognizer.py        # Face recognition engine
│   └── trainer.py           # Model training
├── utils/
│   └── datasets.py          # Dataset utilities
├── main.py                  # Main application
├── setup_and_run.bat        # Automated setup script
├── requirements.txt         # Python dependencies
└── attendance.csv           # Attendance records
```

## Configuration

### Model Parameters
- **Image Size**: 224x224 pixels
- **PCA Variance**: 98% retention
- **Recognition Threshold**: Configurable in recognizer.py
- **Attendance Hold Time**: 2 seconds

### File Paths
All file paths are configured in the respective modules and can be modified:
- Dataset path: `data/images/ml`
- Model path: `models/ml`
- Attendance file: `attendance.csv`

## Troubleshooting

### Common Issues

1. **Camera not detected**
   - Ensure your camera is connected and not used by other applications
   - Try changing camera index in the code (0, 1, 2...)

2. **No faces detected**
   - Ensure good lighting conditions
   - Face should be clearly visible and facing the camera
   - Check if haarcascade file exists in `models/ml/`

3. **Poor recognition accuracy**
   - Collect more training images (20+ per person recommended)
   - Ensure diverse angles and lighting in training data
   - Retrain the model after adding more data

4. **Installation issues**
   - Ensure Python 3.7+ is installed
   - Try creating a fresh virtual environment
   - Install dependencies one by one if batch install fails

### Error Messages

- **"No model found"**: Run the trainer first to create the PCA model
- **"No faces detected"**: Improve lighting or camera position
- **"Dataset is empty"**: Collect face data using data_collector.py first

## Using the Batch Script

The `setup_and_run.bat` file provides an automated way to run the entire pipeline:

### What the batch script does:
1. **Environment Setup**: Activates Python virtual environment
2. **Data Collection**: Guides you through collecting face data
3. **Model Training**: Automatically trains the PCA model
4. **Recognition**: Starts the face recognition system

### How to use:
1. **Double-click** `setup_and_run.bat` in File Explorer
2. **Follow prompts**: The script will guide you through each step
3. **Data Collection**: Enter person details when prompted
4. **Wait for training**: The model will be trained automatically
5. **Start recognition**: The recognition system will launch

### Batch script features:
- ✅ Automatic environment activation
- ✅ Step-by-step guidance
- ✅ Error handling and recovery
- ✅ Progress indicators
- ✅ User-friendly prompts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for computer vision capabilities
- NumPy for numerical computations
- Pandas for data management
- Haar Cascade classifiers for face detection

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Create an issue in the GitHub repository
3. Provide detailed error messages and system information

---

**Happy Face Recognition! 🎯**
