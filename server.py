from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import json
import os
import io
import base64
from keras.models import model_from_json
from datetime import datetime


emozioni = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'neutral': 0, 'sad': 0, 'surprise': 0}
emozioniOrari = []

with open('model/emotion_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()

class_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
emotion_model = model_from_json(loaded_model_json)
emotion_model.load_weights('model/emotion_model.h5')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})


def base64_to_image(base64_string):
    # Rimuovi l'intestazione "data:image/jpeg;base64," o "data:image/png;base64,"
    if base64_string.startswith("data:image/jpeg;base64,"):
        base64_string = base64_string.replace("data:image/jpeg;base64,", "")
    elif base64_string.startswith("data:image/png;base64,"):
        base64_string = base64_string.replace("data:image/png;base64,", "")

    # Decodifica la stringa di base64 in bytes
    image_bytes = base64.b64decode(base64_string)

    # Converti i bytes in un'immagine utilizzando OpenCV
    image_np = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    return image_np


def preprocess_image(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_image = gray_image[y:y + h, x:x + w]
        face_image = cv2.resize(face_image, (48, 48))
        face_image = face_image.astype("float32")
        face_image = face_image / 255.0
        face_image = face_image.reshape((1, 48, 48, 1))

        return face_image
    else:
        return None


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.json:
        return jsonify({'error': 'Nessuna immagine ricevuta'})

    base64_image = request.get_json()['image']
    image = base64_to_image(base64_image)
    status = request.get_json()['status']
    if image is None:
        return jsonify({'error': 'Errore durante la decodifica dell\'immagine'})
    preprocessed_image = preprocess_image(image)
    ritorno = ""
    if preprocessed_image is not None:
        # Esempio: Salva l'immagine preprocessata su disco
        # preprocessed_image_path = "prova.jpg"
        # cv2.imwrite(preprocessed_image_path, preprocessed_image)
        probabilities = emotion_model.predict(preprocessed_image)
        emotion_prediction = class_labels[np.argmax(probabilities, axis=1)[0]]
        aggiungi_emotion(emotion_prediction)
        rileva_emotioni(emotion_prediction)
        ritorno = jsonify({'result': f'{emozioni}'})
    else:
        ritorno = jsonify({'error': 'Nessun volto riconosciuto nell\'immagine'})
    if status == 1:
        directory = 'C:/Users/Carmine/PycharmProjects/EmotionRecognitionForSE4AI-/Report/' + datetime.now().strftime(
            "%Y_%m_%d")
        if not os.path.exists(directory):
            os.makedirs(directory)
        pathJson = directory + '/reportGenerale_' + datetime.now().strftime("%H_%M_%S") + 'lezione.json'
        pathJson2 = directory + '/reportSpecifico_' + datetime.now().strftime("%H_%M_%S") + 'lezione.json'
        # svuotare dizionario
        with open(pathJson, 'w') as file:
            json.dump(emozioni, file)
        with open(pathJson2, 'w') as file:
            json.dump(emozioniOrari, file)
        print(emozioniOrari)
    return ritorno


@app.route('/fileGenerale', methods=['POST'])
def get_fileGenerale():
    data = request.json['report']
    directory = "C:/Users/Carmine/PycharmProjects/EmotionRecognitionForSE4AI-/Report/" + data
    files = os.listdir(directory)
    for file in files:
        if file.startswith('reportGenerale'):
            percorso_file = os.path.join(directory, file)
            with open(percorso_file, 'r') as file2:
                file_content = json.load(file2)
                return jsonify(file_content)
            break
    return jsonify({'error': 'File not found'})


@app.route('/fileSpecifico', methods=['POST'])
def get_fileSpecifico():
    data = request.json['report']
    directory = "C:/Users/Carmine/PycharmProjects/EmotionRecognitionForSE4AI-/Report/" + data
    files = os.listdir(directory)
    for file in files:
        if file.startswith('reportSpecifico'):
            percorso_file = os.path.join(directory, file)
            print(percorso_file)
            with open(percorso_file, 'r') as file2:
                file_content = json.load(file2)
                return jsonify(file_content)
            break
    return jsonify({'error': 'File not found'})


def aggiungi_emotion(emotion):
    if emotion in emozioni:
        emozioni[emotion] += 1  # Incrementa il contatore dell'emozione


def rileva_emotioni(emoji):
    ora_corrente = datetime.now().strftime("%H:%M:%S")
    emozione_ora = {emoji: ora_corrente}
    emozioniOrari.append(emozione_ora)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
