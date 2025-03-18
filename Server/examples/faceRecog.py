# Initial attempt at face detection(Haar cascades) and recognition(LBPH) using openCV

# Example code for face detection and recognition using opencv
# Largely referenced code at :
# https://towardsdatascience.com/real-time-face-recognition-an-end-to-end-project-b738bb0f7348
# https://www.superdatascience.com/blogs/opencv-face-recognition

# Download the haar classifier at
# https://github.com/opencv/opencv/tree/master/data/haarcascades
# and save it to the directory of this program.

import cv2 as cv
import numpy as np
import os

#Detect faces w/ Haar Cascade Classifier, draw a box around them, and identify them w/ LBPH
def faceDetection(model):
    cv.namedWindow("frame", cv.WINDOW_NORMAL)
    # Load classifier
    # Different classifiers available at: https://github.com/opencv/opencv/tree/master/data/haarcascades
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

    #0 for default camera(synced to iphone (settings->continuity camera), then switched to webcam after disconnect)
    cap = cv.VideoCapture(0)

    while(True):
        valid, frame = cap.read()
        if valid:
            print("Valid frame")
            extracted_faces, coordinates = extractFace(frame, face_cascade)

            if len(extracted_faces)>0:
                print(f"face count: {len(extracted_faces)}")
                for face, coordinate in zip(extracted_faces, coordinates):
                    #want low confidence value
                    face_id, confidence = predictFace(model,face)
                    confidence = np.floor(confidence)
                    cv.putText(frame, str(face_id), (coordinate[0]+5,coordinate[1]-5),cv.FONT_HERSHEY_SIMPLEX, 4, (50,205,0), 4)
                    cv.putText(frame, str(confidence), (coordinate[0]+coordinate[3],coordinate[1]-5),cv.FONT_HERSHEY_SIMPLEX, 2, (50,205,0), 4)
                    print(f"ID: {face_id}, Confidence: {confidence}\n")
                print("===============")

            cv.imshow('frame',frame)
        else:
            print("Invalid")
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


# Return grayscale faces extracted from image
# Also draw a box around them in the frame
def extractFace(frame, face_cascade):
    extracted_faces = []
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #https://stackoverflow.com/questions/36218385/parameters-of-detectmultiscale-in-opencv-using-python
    faces = face_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv.rectangle(frame,(x,y),(x+w,y+h),(50,225,0),5) #draw rectangle around detected face
        extracted_faces.append(gray_image[y:y+h, x:x+w])

    return extracted_faces, faces


# Predict the id of a grayscale face
def predictFace(model, face):
    face_id, confidence = model.predict(face)
    # print(f"ID: {faceId}, Confidence: {confidence}\n")
    return face_id, confidence

# Procure grayscale faces from person w/ given id and save to local directory
def getTrainingData(path, face_id, samples):
    cv.namedWindow("frame", cv.WINDOW_NORMAL)
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv.VideoCapture(0)

    face_samples = []
    while(samples > 0):
        valid, frame = cap.read()
        if valid:
            print("Valid frame")
            extracted_faces, _ = extractFace(frame, face_cascade)
            print(f"face count: {len(extracted_faces)}")
            if len(extracted_faces) == 1:
                samples -= 1
                # save as path/id_sampleNumber.jpg
                cv.imwrite(path + "/" + str(face_id) + "_" + str(samples) + ".jpg", extracted_faces[0])
                face_samples.append(extracted_faces[0])
            cv.imshow('frame',frame)
        else:
            print("Invalid")
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


# Use saved face data to train recognizer (-> .yml file)
def trainModel(path):
    image_paths = [os.path.join(path,f) for f in os.listdir(path)]
    face_samples=[]
    ids = []

    # Upload all samples of all ids
    for image_path in image_paths:
        if os.path.basename(image_path).split(".")[-1] != "jpg":
            print(os.path.basename(image_path).split("_")[-1])
            continue

        gray_face = cv.imread(image_path, flags=cv.IMREAD_GRAYSCALE)
        print(gray_face)
        print(gray_face.shape)
        print("++++++++++++++++")
        ids.append(int(os.path.basename(image_path).split("_")[0]))
        face_samples.append(gray_face)

    model = cv.face.LBPHFaceRecognizer_create()
    model.train(face_samples, np.array(ids))
    model.write('trainer.yml')


if __name__ == '__main__':
    # Use the first function for every person; change the id
    getTrainingData("face_data", 0, 50)
    trainModel("face_data")

    # To run the model on live feed, uncomment the lines below:
    # model = cv.face.LBPHFaceRecognizer_create()
    # model.read("trainer.yml")
    # faceDetection(model)

    cv.destroyAllWindows()


