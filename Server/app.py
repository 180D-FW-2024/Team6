from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from flask_cors import CORS
import cv2
from deepface import DeepFace
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
import os
import io
import pandas as pd
import datetime

import mongodb as db
# import bcrypt


app = Flask(__name__)
CORS(app, supports_credentials=True)

# Folder where known faces are stored, each subdirectory is a person
KNOWN_FACES_DIR = './static/known_faces'
RECVD_FACES_DIR = './static/recvd_faces'
CSV_FILE = "voice_memos.csv"

DEFAULT_LOCK_ID = "-1"


# face_recognizer = cv2.face.LBPHFaceRecognizer_create()
db.initDB()

label_map = {}
current_label = 0
training_data = []
labels = []

# Ensure required directory and file exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

if not os.path.exists(RECVD_FACES_DIR):
    os.makedirs(RECVD_FACES_DIR)

if not os.path.exists(CSV_FILE):
    # Create a new CSV file with a basic structure
    pd.DataFrame(columns=["Timestamp", "Memo"]).to_csv(CSV_FILE, index=False)

'''
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
'''

# Sample route to fetch door status
@app.route('/api/door_status', methods=['GET'])
def door_status():
    # Return current door status
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    return jsonify(db.getDoorState(lock_id))

# Sample route to get voice memos
@app.route('/api/voice_memos', methods=['GET'])
def voice_memos():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    return jsonify(db.getMemos(lock_id))

# Delete the memo with the specified object id
@app.route('/api/delete_memo', methods=['POST'])
def delete_memo():
    memo_id = request.json['memo_id']
    db.deleteMemo(memo_id)
    return ''

# Sample route to get visitor images as base64 strings
@app.route('/api/visitors', methods=['GET'])
def visitors():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    return jsonify(db.getVisitors(lock_id))

# Delete the photos with the specified photo ids
# and return the remaining photos
@app.route('/api/delete_photo', methods=['POST'])
def delete_photo():
    # print(request.json)
    image_id = request.json['image_id']
    db.deleteVisitor(image_id)
    return ''

# Get authorized faces(residents) for this lock id
@app.route('/api/residents', methods=['GET'])
def residents():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    return jsonify(db.getResidents(lock_id))

# Delete the authorized person's images from this lock_id
# (Delete method has issues with sending headers...cookies could not be read)
# Also updates local known_faces
@app.route('/api/delete_resident', methods=['POST'])
def delete_resident():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    # Update database
    name = request.json['name']
    db.deleteResident(name, lock_id)
    # Delete local files
    path = KNOWN_FACES_DIR+"/"+str(lock_id)+"/" + name + "/"
    for filename in os.listdir(path):
        os.remove(path + filename)
    os.rmdir(path)
    return ''

# Add visitor images to an existing resident of this lock_id
# or create a new resident with the given name
# Also updates local known_faces
@app.route('/api/add_resident', methods=['POST'])
def addresident():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    name = request.json['newName']
    image_ids = request.json['image_ids']
    # Update database
    db.addResident(lock_id, name, image_ids)
    # Load new files (overwrite)
    db.downloadKnownFaces(lock_id,KNOWN_FACES_DIR)
    return ''


# Toggle lock status
@app.route("/toggle", methods=["POST"])
def toggle():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    db.toggleLock(lock_id, request.json['door_unlocked'])
    return redirect(url_for("display"))

@app.route("/")
def display():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    # Load memos
    memos = db.getMemos(lock_id)

    # Load image data
    visitor_photos = db.getVisitors(lock_id)

    # Load door status
    state = db.getDoorState(lock_id)

    # Render the page
    return render_template("index.html", door_state=state, memos=memos, 
                           visitor_photos=visitor_photos)

# Using DeepFace recognition (VGG-Face)
@app.route('/receive', methods=['POST'])
def receive_image():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 302
    
    # load training data from DB if not already locally saved
    if not os.path.exists(KNOWN_FACES_DIR +'/' + str(lock_id)):
        db.downloadKnownFaces(lock_id,KNOWN_FACES_DIR)


    file = request.files['image']
    img_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_np, cv2.IMREAD_COLOR) # deepface uses BGR images

    # Save the image locally and in the DB
    cv2.imwrite(RECVD_FACES_DIR + "/" + datetime.datetime.now().strftime("%m-%d-%Y_%H.%M.%S") + ".jpg", image)
    db.addVisitor(lock_id, image, None)

    try:
        # returns a pandas data frame
        dfs = DeepFace.find(
            img_path = image,
            db_path = KNOWN_FACES_DIR + "/"+str(lock_id),
            threshold = 0.55,
            model_name = 'VGG-Face',
            detector_backend = 'opencv', # opencv
            distance_metric = 'cosine',
            enforce_detection=False,
            # align = True  # on by default
            # anti_spoofing = True  #ends up discarding a lot of photos
        )
    except ValueError:
        print("no face detected")
        return jsonify({'error': 'No face detected'}), 300
    
    # no faces matched
    # lock door if unconfident
    if len(dfs[0]) == 0:
        print("Nobody")
        db.lockDoor(lock_id)
        return jsonify({'error': 'Unknown face'}), 301
    
    temp = dfs[0].loc[0, :]
    path, _ = os.path.split(temp['identity'])
    _, matched_name = os.path.split(path)
    confidence = temp['distance']

    if confidence > 0.5:
        print("Not confident enough (%s, %f)" % (matched_name, confidence))
        db.lockDoor(lock_id)
        return jsonify({'error': 'Unknown face(not confident enough)'}), 301
    
    # unlock door if recognized face
    db.unlockDoor(lock_id)
    print(confidence)
    print(matched_name)
    return jsonify({'name': matched_name, 'confidence': confidence})
    
'''
# Old endpoint using OpenCV face recognition
@app.route('/receive', methods=['POST'])
def receive_image():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 302

    file = request.files['image']
    img_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_np, cv2.IMREAD_GRAYSCALE)

    # Save the image locally and in the DB
    cv2.imwrite(RECVD_FACES_DIR + "/" + datetime.datetime.now().strftime("%m-%d-%Y_%H.%M.%S") + ".jpg", image)
    db.addVisitor(lock_id, image, None)

    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return jsonify({'error': 'No face detected'}), 300

    x, y, w, h = faces[0]
    face_to_recognize = image[y:y + h, x:x + w]

    face_to_recognize = image
    label, confidence = face_recognizer.predict(face_to_recognize)

    if confidence < 80:  # Face recognized (want confidence beneath threshold)
        matched_name = label_map.get(label, "Unknown")
        db.unlockDoor(lock_id)
        print(confidence)
        print(matched_name)
        
        return jsonify({'name': matched_name, 'confidence': confidence})
    else:
        print("nobody")
        print(confidence)
        return '', 301
'''
    
@app.route('/receiveaudio', methods=['POST'])    
def receive_audio():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
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
        db.addMemo(lock_id, text, timestamp)
        print("Heard: ", text) # debugging
        return jsonify({'transcription': text})
    except sr.UnknownValueError:
        print("Could not understand audio") # debugging
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError:
        print("Could not request results from the speech recognition service")  # debugging
        return jsonify({'error': 'Could not request results from the speech recognition service'}), 500

# From Rpi: receive current door position
@app.route('/receiveposition', methods=['POST'])
def receive_open():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    state = request.form['position']
    db.setOpenState(lock_id, state == 'open')
    return '', 200

# To Rpi: reply with lock status
@app.route("/getunlocked", methods=["GET"])
def get_unlocked():
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    state = db.getDoorState(lock_id)
    return jsonify({'door_unlocked': state['door_unlocked']})

@app.route('/login', methods=['POST'])
def login():
    print(request.headers)  # Debugging: Print request headers
    print(request.get_data())  # Debugging: Print raw request data

    data = request.json  # Use request.json instead of request.form
    print(f"Received data: {data}")  # Debugging: Print parsed data

    username = data.get('username')
    password = data.get('password')

    # print("ccokies:" )
    # print(request.cookies)

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if db.verifyLock(username, password):
        print(f"Successful login for username: {username}")
        lock_id = db.getLockid(username)
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('username', username, httponly=True, samesite='Lax')
        resp.set_cookie('lock_id', str(lock_id), httponly=True, samesite='Lax')
        
        # Load authorized faces(residents) of this lock to local file system
        print("Fetching resident faces for " + str(lock_id))
        db.downloadKnownFaces(lock_id,KNOWN_FACES_DIR)

        return resp
    else:
        print(f"Invalid login attempt for username: {username}")
        return jsonify({"error": "Invalid username or password"}), 401
    
@app.route('/check_login', methods=['GET'])
def check_login():
    username = request.cookies.get('username')
    if username:
        # Load authorized faces(residents) of this lock to local file system
        lock_id = db.getLockid(username)
        print("Fetching resident faces for " + str(lock_id))
        # db.downloadKnownFaces(lock_id,KNOWN_FACES_DIR) #only download on login
        return jsonify({"logged_in": True, "username": username})
    else:
        return jsonify({"logged_in": False}), 401

@app.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({"message": "Logged out successfully"})
    resp.set_cookie('username', '', expires=0)  # Clears the cookie
    return resp

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    id = data.get('id')

    if not username or not password or not id:
        return jsonify({"error": "Username and password required"}), 400

    if db.addLock(username, password, int(id)):
        print(f"Successfully signed up for username: {username}")
        return jsonify({"message": "User created successfully"}), 201
    else:
        print(f"Failed to sign up for username: {username}")
        return jsonify({"error": "User already exists"}), 409
    
@app.route('/dashboard')
def dashboard():
    username = request.cookies.get('username')  # Get username from cookies
    print("Received username from cookie:", username)

    if not username:
        return redirect(url_for('login'))  # Redirect to login if no user is found

    # Fetch door status, voice memos, and visitor data
    lock_id = int(request.cookies.get('lock_id', DEFAULT_LOCK_ID))
    door_status = db.getDoorState(lock_id) or {}
    voice_memos = db.getMemos(lock_id) or []
    visitors = db.getVisitors(lock_id) or []

    return render_template("dashboard.html", 
                           door_status=door_status, 
                           voice_memos=voice_memos, 
                           visitors=visitors)


@app.route('/update_username', methods=['POST'])
def update_username():
    data = request.json
    old_username = data.get('old_username')
    new_username = data.get('new_username')

    if not old_username or not new_username:
        return jsonify({"error": "Both old and new usernames are required"}), 400

    success = db.updateUsername(old_username, new_username)
    if success:
        resp = jsonify({"message": "Username updated successfully"})
        resp.set_cookie('username', new_username, httponly=True, samesite='Lax')  # Update cookie
        return resp
    else:
        return jsonify({"error": "Failed to update username"}), 500


@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({"error": "All fields are required"}), 400

    success = db.updatePassword(username, old_password, new_password)
    if success:
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update password"}), 401



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
