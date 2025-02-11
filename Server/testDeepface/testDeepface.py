# pip install deepface
# tf-keras

# Had to move
# haarcascade_eye.xml and haarcascade_frontalface_default.xml
# to /miniconda3/envs/yourenvname/lib/python3.12/site-packages/data/

from deepface import DeepFace
import os
import cv2


# compare 2 images
# verification = DeepFace.verify(img1_path = "test_yin.jpg",
# 	img2_path = "test4.jpg",
# 	align = True
# 	# model_name = "Facenet"
# 	)
# print(verification)


# compare against multiple images (returns pandas dataframe)
# dfs = DeepFace.find(
#   img_path = "test_yin2.jpg",
#   db_path = "../static/known_faces",	# it says we're very alike...ok
#   # model_name = "Facenet"
# )
# print(dfs)

TRAIN_DIR = "./known_faces"
TEST_DIR = "./test_data"
models = [
  "VGG-Face",
  "Facenet",
  "Facenet512",
  "OpenFace",
  "DeepFace",
  "DeepID",
  "ArcFace",
  "Dlib",
  "SFace",
  "GhostFaceNet",
]
# for face detection & alignment
backends = [
  'opencv',
  'ssd',
  'dlib',
  'mtcnn',
  'fastmtcnn',
  'retinaface',
  'mediapipe',
  'yolov8',
  'yunet',
  'centerface',
]
# for loss
metrics = ["cosine", "euclidean", "euclidean_l2"]

correct={}
totals={}
unclassified=[]
totalImages=0
totalCorrect=0 # true positives and negatives
falsePositives=0


# Predict person in each person folder in the test data
for person_name in os.listdir(TEST_DIR):
  person_dir = os.path.join(TEST_DIR, person_name)
  if os.path.isdir(person_dir):
    # ...

    for filename in os.listdir(person_dir):
      if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(person_dir, filename)

        try:
          # Compare against training data
          image_np = cv2.imread(image_path,  cv2.IMREAD_COLOR)

          dfs = DeepFace.find(
            img_path = image_np,
            db_path = TRAIN_DIR,
            threshold = 0.5,
            model_name = models[2],
            detector_backend = backends[0], # opencv
            distance_metric = metrics[0],
            # align = True  # on by default
            # anti_spoofing = True  #ends up discarding a lot of photos
          )

          # Update accuracy scores
          if person_name not in totals:
            totals[person_name] = 0
            correct[person_name] = 0

          totals[person_name]+=1 # unclassified faces also reduce a person's accuracy score
          totalImages+=1

          if len(dfs[0]) == 0:
            if person_name == 'Unknown':
              correct[person_name] += 1
              totalCorrect+=1
            unclassified.append(image_path)
          else:
            # get closest match and check against label
            temp = dfs[0].loc[0, :]
            path, _ = os.path.split(temp['identity'])
            _, pred_label = os.path.split(path)
            if person_name == pred_label:
              correct[person_name] += 1
              totalCorrect += 1
            else:
              falsePositives+=1


          # print(">>>TESTING:" + person_name +'(' + image_path +')')
          # Evalulate predicted label accuracy
          # for i in range(0,min(1, len(dfs[0]))):
          #   temp = dfs[0].loc[i, :]
          #   path, _ = os.path.split(temp['identity'])
          #   _, pred_label = os.path.split(path)

          #   print(pred_label)
          #   print(temp['distance'])

        except ValueError:
          print("Could not find face for: " + image_path)
      print("====================")

for key in totals.keys():
  print("%s: %f" % (key, 1.0*correct[key]/totals[key]))
print("Overall accuracy: %f" % (totalCorrect/totalImages))
print("False positives: %f" % (falsePositives/totalImages))
print("unclassified: %d of %d total (%f)" %(len(unclassified), totalImages, len(unclassified)/totalImages))
# print("unclassified", unclassified)


