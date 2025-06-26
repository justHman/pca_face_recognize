import cv2

CASCADE_PATH = r'models\ml\haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def detect_faces(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30) 
    )
    
    return faces

def crop_face(image, bbox):
    x, y, w, h = bbox
    return image[y:y+h, x:x+w]