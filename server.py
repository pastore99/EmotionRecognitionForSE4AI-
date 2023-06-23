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
from PIL import Image

data_corrente = datetime.now().date()
with open('model/emotion_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()

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

        # face_image = face_image / 255.0
        face_image = np.expand_dims(face_image, axis=-1)
        return face_image
    else:
        return None

@app.route('/preprocessBase64', methods=['POST'])
def preprocessBase64():
    if 'image' not in request.json:
        return jsonify({'error': 'Nessuna immagine ricevuta'})

    base64_image = request.get_json()['image']
    image = base64_to_image(base64_image)
    if image is None:
        return jsonify({'error': 'Errore durante la decodifica dell\'immagine'})
    preprocessed_image = preprocess_image(image)

    if preprocessed_image is not None:
        # Esempio: Salva l'immagine preprocessata su disco
        preprocessed_image_path = "prova.jpg"
        cv2.imwrite(preprocessed_image_path, preprocessed_image)
        #emotion_prediction = emotion_model.predict(preprocessed_image)
        return jsonify({'result': 'Immagine preprocessata salvata correttamente'})
    else:
        return jsonify({'error': 'Nessun volto riconosciuto nell\'immagine'})


@app.route('/salva_report', methods=['POST'])
def salva_report():
    dati_report = request.get_json()
    pathJson = 'report_' + data_corrente + 'lezione_' +'.json'  # il file json avra nel nome un identificativo che cambierà in base alla lezione, questo per permettere la creazione di charts per ogni lezione
    dati_esistenti2 = []
    if os.path.exists(pathJson):
        with open(pathJson, 'r') as file:
            dati_esistenti = json.load(file)

    dati_esistenti2.append(dati_esistenti)
    dati_esistenti2.append(dati_report)
    print(dati_esistenti2)

    with open(pathJson, 'w') as file:
        json.dump(dati_esistenti, file)

    return jsonify({'message': 'Report salvato con successo'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
