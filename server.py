from tkinter import Image
from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)


def preprocess_image(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_image = gray_image[y:y + h, x:x + w]
        face_image = cv2.resize(face_image, (48, 48))
        # face_image = face_image / 255.0
        face_image = np.expand_dims(face_image, axis=-1)
        return face_image
    else:
        return None


@app.route('/preprocess', methods=['POST'])
def preprocess():
    if 'image' not in request.files:
        return jsonify({'error': 'nessun file di immagine ricevuto'})
    image_file = request.files['image']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    preprocessed_image = preprocess_image(image)
    if preprocessed_image is not None:
        preprocessed_image_path = r"C:\Users\Carmine\OneDrive\Desktop\provaPY\immagine.jpg"
        cv2.imwrite(preprocessed_image_path, preprocessed_image)
        return jsonify({'result': preprocessed_image.tolist()})
    else:
        return jsonify({'error': 'No face detected in the image'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)