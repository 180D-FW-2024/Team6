# Helper script to upload local training data to database (append)
import os
import cv2
import mongodb as db


KNOWN_FACES_DIR = './static/known_faces'
LOCK_ID = 1

db.initDB()

# Below block to upload all known_faces to DB (appends)
lock_dir = os.path.join(KNOWN_FACES_DIR, str(LOCK_ID))
for person_name in os.listdir(lock_dir):
    person_dir = os.path.join(lock_dir, person_name)
    if os.path.isdir(person_dir):
        # Process each image for the person
        for filename in os.listdir(person_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(person_dir, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                db.uploadKnownFace(LOCK_ID, image, person_name)
                print("Uploaded: " +  image_path)


# This line downloads all known faces ("residents") from the DB (appends)
# db.downloadKnownFaces(LOCK_ID,KNOWN_FACES_DIR)