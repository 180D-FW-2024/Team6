from flask import Flask, request, jsonify
import cv2
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
import os
import io

app = Flask(__name__)

# Folder where known faces are stored, each subdirectory is a person
KNOWN_FACES_DIR = 'known_faces'
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
label_map = {}
current_label = 0
training_data = []
labels = []

# Load images and labels from subdirectories in KNOWN_FACES_DIR
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

for person_name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, person_name)
    if os.path.isdir(person_dir):
        # Assign a unique label for each person
        if person_name not in label_map.values():
            label_map[current_label] = person_name
            person_label = current_label
            current_label += 1
        else:
            # Skip if the person's label is already assigned
            continue

        # Process each image for the person
        for filename in os.listdir(person_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(person_dir, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

                # Only use the first detected face in each image for simplicity
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_region = image[y:y + h, x:x + w]
                    training_data.append(face_region)
                    labels.append(person_label)

# Train face recognizer
if training_data:
    face_recognizer.train(training_data, np.array(labels))

@app.route('/receive', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    img_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_np, cv2.IMREAD_GRAYSCALE)

    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return jsonify({'error': 'No face detected'}), 400

    x, y, w, h = faces[0]
    face_to_recognize = image[y:y + h, x:x + w]

    label, confidence = face_recognizer.predict(face_to_recognize)
    if confidence < 100:  # Adjust threshold based on your needs
        matched_name = label_map.get(label, "Unknown")
        return jsonify({'name': matched_name, 'confidence': confidence})
    else:
        return jsonify({'name': 'Unknown', 'confidence': confidence})
    
@app.route('/receiveaudio', methods=['POST'])    
def receive_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['audio']
    recognizer = sr.Recognizer()

    # Convert the audio file to WAV format if needed
    audio_format = file.filename.split('.')[-1].lower()
    audio_data = io.BytesIO(file.read())

    if audio_format != 'wav':
        # Convert non-WAV formats to WAV
        audio = AudioSegment.from_file(audio_data, format=audio_format)
        audio_data = io.BytesIO()
        audio.export(audio_data, format="wav")
        audio_data.seek(0)

    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)

    try:
        # Recognize the speech in the audio
        text = recognizer.recognize_google(audio)
        return jsonify({'transcription': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError:
        return jsonify({'error': 'Could not request results from the speech recognition service'}), 500


if __name__ == '__main__':
    app.run(debug=True)
