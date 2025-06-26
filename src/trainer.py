import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.datasets import face_dataset_ml

DATASET_PATH = r'data\images\ml'
MODEL_PATH = r'models\ml'

WIDTH = 224 
HEIGHT = 224

def train_pca_model():
    print("Bắt đầu quá trình huấn luyện model...")
    
    train_dataset = face_dataset_ml(root='data\images\ml')
    image_matrix = np.array([train_dataset[idx][0].flatten() for idx in range(len(train_dataset))], dtype=np.float32)
    labels = np.array(train_dataset.labels)
    maps = train_dataset.maps

    mean, eigenvectors = cv2.PCACompute(image_matrix, mean=None, retainedVariance=0.98)
    projected_data = cv2.PCAProject(image_matrix, mean, eigenvectors)
    print(eigenvectors.shape)

    model_file = os.path.join(MODEL_PATH, 'pca_model.npz')
    np.savez(
        model_file,
        mean=mean,
        eigenvectors=eigenvectors,
        projected_data=projected_data,
        labels=labels,
        maps=maps 
    )
    
    print(f"Huấn luyện hoàn tất! Model đã được lưu tại: {model_file}")
    print(f"Số lượng người trong model: {len(maps)}")
    return True

if __name__ == '__main__':
    train_pca_model()