import cv2
import os
from flask import Flask, request, jsonify
from src.face_detector import detect_faces, crop_face
from src.recognizer import Recognizer

app = Flask(__name__)
recognizer = Recognizer()

@app.route("/recognize", methods=["POST"])
def recognize_face():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]
        image_path = os.path.join("temp", file.filename)
        os.makedirs("temp", exist_ok=True)
        file.save(image_path)
        image = cv2.imread(image_path)
        if image is None:
            os.remove(image_path)
            return jsonify({"error": "Cannot read image"}), 400

        faces_coords = detect_faces(image)
        if len(faces_coords) == 1:
            (x, y, w, h) = faces_coords[0]
            face_img = crop_face(image, (x, y, w, h))
            id, name, distance = recognizer.recognize(face_img)
            os.remove(image_path)
            return jsonify({"id": id, "name": name})
        else:
            os.remove(image_path)
            return jsonify({"error": "Require exactly one face in frame"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def homepage():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Face Recognition API</title>
    </head>
    <body>
        <h2>Face Recognition API</h2>
        <p>Use the /recognize endpoint to recognize faces.</p>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(port=5000)