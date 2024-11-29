from flask import Flask, request, jsonify, render_template, redirect, url_for
import cv2
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
import os
import io
import pandas as pd
import datetime

app = Flask(__name__, static_url_path='/static')

# Folder where known faces are stored, each subdirectory is a person
KNOWN_FACES_DIR = './static/known_faces'
RECVD_FACES_DIR = './static/recvd_faces'
CSV_FILE = "voice_memos.csv"

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
label_map = {}
current_label = 0
training_data = []
labels = []

door_unlocked = True
door_open = True

# Ensure required directory and file exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

if not os.path.exists(RECVD_FACES_DIR):
    os.makedirs(RECVD_FACES_DIR)

if not os.path.exists(CSV_FILE):
    # Create a new CSV file with a basic structure
    pd.DataFrame(columns=["Timestamp", "Memo"]).to_csv(CSV_FILE, index=False)

# Load images and labels from subdirectories in KNOWN_FACES_DIR
face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

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


@app.route("/toggle", methods=["POST"])
def toggle():
    global door_unlocked
    # Toggle the door_unlocked variable
    door_unlocked = not door_unlocked
    return redirect(url_for("display"))




@app.route("/")
def display():
    global door_unlocked, door_open
    # Load CSV data
    try:
        df = pd.read_csv("voice_memos.csv")
        csv_html = df.to_html(index=False, classes="table table-striped")
    except FileNotFoundError:
        csv_html = "<p>No voice_memos.csv file found.</p>"

    # Load image data
    recvd_faces_paths = os.listdir(RECVD_FACES_DIR)
    
    # Render the page
    return render_template("index.html", door_unlocked=door_unlocked, door_open=door_open, csv_html=csv_html,
        recvd_faces_paths=recvd_faces_paths)


@app.route('/receive', methods=['POST'])
def receive_image():
    global door_unlocked
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 302

    file = request.files['image']
    img_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_np, cv2.IMREAD_GRAYSCALE)

    # Also save the image
    cv2.imwrite(RECVD_FACES_DIR + "/" + datetime.datetime.now().strftime("%m-%d-%Y_%H.%M.%S") + ".jpg", image)

    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return jsonify({'error': 'No face detected'}), 300
    
    #Integrate face recognition later:

    x, y, w, h = faces[0]
    face_to_recognize = image[y:y + h, x:x + w]

    face_to_recognize = image
    label, confidence = face_recognizer.predict(face_to_recognize)
    if confidence < 80:  # Adjust threshold based on your needs
        matched_name = label_map.get(label, "Unknown")
        door_unlocked = True
        print(confidence)
        print(matched_name)
        
        return jsonify({'name': matched_name, 'confidence': confidence})
    else:
        print("nobody")
        print(confidence)
        return '', 301
    return '', 200 ###
    
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
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CSV_FILE, 'a') as f:
            f.write(f"{timestamp}, {text}\n")
        return jsonify({'transcription': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError:
        return jsonify({'error': 'Could not request results from the speech recognition service'}), 500

# From Rpi
@app.route('/receiveposition', methods=['POST'])
def receive_open():
    global door_open
    state = request.form['position']
    # print(request.form)
    door_open = (state == 'unlocked')
    return '', 200

@app.route("/getunlocked", methods=["GET"])
def get_unlocked():
    global door_unlocked
    return jsonify({'door_unlocked': door_unlocked})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
