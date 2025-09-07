@echo off
setlocal EnableDelayedExpansion

:: Set console colors and title
title Face Recognition System - Automated Setup
color 0A

:: Display banner
echo.
echo ===============================================
echo    Face Recognition System - Automated Setup
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ and add it to your PATH
    echo.
    pause
    exit /b 1
)

echo [INFO] Python detected successfully
echo.

:: Create and activate virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
    echo.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

:: Install requirements
echo [INFO] Installing required packages...
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)
echo [SUCCESS] All packages installed successfully
echo.

:: Create necessary directories
if not exist "data\images\ml" mkdir "data\images\ml"
if not exist "models\ml" mkdir "models\ml"

:: Main menu loop
:MAIN_MENU
echo ===============================================
echo              MAIN MENU
echo ===============================================
echo 1. Collect Face Data (Step 1)
echo 2. Train Recognition Model (Step 2)
echo 3. Start Face Recognition (Step 3)
echo 4. Run Complete Pipeline (1→2→3)
echo 5. Exit
echo ===============================================
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto DATA_COLLECTION
if "%choice%"=="2" goto TRAINING
if "%choice%"=="3" goto RECOGNITION
if "%choice%"=="4" goto FULL_PIPELINE
if "%choice%"=="5" goto EXIT
echo [ERROR] Invalid choice. Please select 1-5.
goto MAIN_MENU

:DATA_COLLECTION
echo.
echo ===============================================
echo            STEP 1: DATA COLLECTION
echo ===============================================
echo.
echo Instructions:
echo - Enter person information as: ID-Name (e.g., SE194190-John)
echo - Look directly at the camera
echo - System will capture 20 images automatically
echo - Press 'q' to quit or 'n' for next person
echo.
pause

python src\data_collector.py
if errorlevel 1 (
    echo [ERROR] Data collection failed
    pause
    goto MAIN_MENU
)

echo.
echo [SUCCESS] Data collection completed!
echo.
pause
goto MAIN_MENU

:TRAINING
echo.
echo ===============================================
echo           STEP 2: MODEL TRAINING
echo ===============================================
echo.

:: Check if there's training data
if not exist "data\images\ml\*" (
    echo [ERROR] No training data found!
    echo Please run Step 1 (Data Collection) first.
    echo.
    pause
    goto MAIN_MENU
)

echo [INFO] Training PCA model with collected data...
echo This may take a few moments...
echo.

python src\trainer.py
if errorlevel 1 (
    echo [ERROR] Model training failed
    pause
    goto MAIN_MENU
)

echo.
echo [SUCCESS] Model training completed!
echo Model saved to: models\ml\pca_model.npz
echo.
pause
goto MAIN_MENU

:RECOGNITION
echo.
echo ===============================================
echo          STEP 3: FACE RECOGNITION
echo ===============================================
echo.

:: Check if model exists
if not exist "models\ml\pca_model.npz" (
    echo [ERROR] No trained model found!
    echo Please run Step 2 (Model Training) first.
    echo.
    pause
    goto MAIN_MENU
)

echo Instructions:
echo - Green rectangle = Recognized person
echo - Red rectangle = Unknown person  
echo - Hold position for 2 seconds to mark attendance
echo - Press 'q' to quit the application
echo.
echo [INFO] Starting face recognition system...
echo.

python main.py
if errorlevel 1 (
    echo [ERROR] Face recognition system encountered an error
    pause
    goto MAIN_MENU
)

echo.
echo [INFO] Face recognition system closed
echo.
pause
goto MAIN_MENU

:FULL_PIPELINE
echo.
echo ===============================================
echo           COMPLETE PIPELINE
echo ===============================================
echo.
echo This will run all steps in sequence:
echo 1. Data Collection
echo 2. Model Training  
echo 3. Face Recognition
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto MAIN_MENU

:: Step 1: Data Collection
echo.
echo [PIPELINE] Step 1/3: Data Collection
echo ===============================================
echo.
echo Instructions for data collection:
echo - Enter person information as: ID-Name
echo - Look directly at the camera
echo - System will capture images automatically
echo - Press 'q' when done with all people
echo.
pause

python src\data_collector.py
if errorlevel 1 (
    echo [ERROR] Data collection failed - Pipeline stopped
    pause
    goto MAIN_MENU
)

:: Step 2: Training
echo.
echo [PIPELINE] Step 2/3: Model Training
echo ===============================================
echo.
echo [INFO] Training model with collected data...
python src\trainer.py
if errorlevel 1 (
    echo [ERROR] Model training failed - Pipeline stopped
    pause
    goto MAIN_MENU
)

:: Step 3: Recognition
echo.
echo [PIPELINE] Step 3/3: Face Recognition
echo ===============================================
echo.
echo [SUCCESS] Pipeline completed successfully!
echo Starting face recognition system...
echo.
echo Instructions:
echo - Green rectangle = Recognized person
echo - Red rectangle = Unknown person
echo - Hold position for 2 seconds to mark attendance  
echo - Press 'q' to quit
echo.
pause

python main.py
if errorlevel 1 (
    echo [ERROR] Face recognition system encountered an error
)

echo.
echo [INFO] Complete pipeline finished
echo.
pause
goto MAIN_MENU

:EXIT
echo.
echo ===============================================
echo Thank you for using Face Recognition System!
echo ===============================================
echo.

:: Check if attendance file was created
if exist "attendance.csv" (
    echo [INFO] Attendance records saved in: attendance.csv
)

echo Deactivating virtual environment...
deactivate
echo.
echo Press any key to exit...
pause >nul
exit /b 0

:ERROR_HANDLER
echo.
echo [ERROR] An unexpected error occurred
echo Please check the error messages above
echo.
pause
goto MAIN_MENU
