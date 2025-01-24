from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from base64 import b64encode
import time
import datetime
import cv2

# Using Mongo DB Atlas
# Login gmail: locked.in.db@gmail.com
# Password: ece180dw
uri = "mongodb+srv://lockedindb:ece180dw@appdb.gwoxs.mongodb.net/?retryWrites=true&w=majority&appName=AppDB"
db = None


def initDB():
    global db
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.LockDB # database

    time.sleep(1)

    # For testing -- note: there is a reload after initialization
    # if verifyUser("person a", "a") and not verifyUser("person a", "wrong"):
    #     print("verify success")
    # else:
    #     print("verify wrong")

    # img = cv2.imread("static/recvd_faces/orange.png")
    # addVisitor("person a", img, datetime.datetime.now())
    # img = cv2.imread("static/recvd_faces/11-28-2024_22.52.28.jpg")
    # addVisitor("person a", img, datetime.datetime.now())



def verifyUser(user, password):
    return db.Users.find_one({"name" : user})['password'] == password


# Return array of images encoded as base-64 strings(timestamp and data)
def getVisitors(user):

    photos = db.Visitors.find({"user_name" : user})

    # convert image bytes to string
    # photo['title'] = b64encode(...) does not work, so create separate array
    photoArray = []
    for photo in photos:
        photoArray.append({"timestamp" : photo['timestamp'], "data" : b64encode(photo['data']).decode('utf-8')})

    return photoArray

# Add a photo taken by some user's camera
def addVisitor(user, img, timestamp = None):
    if timestamp == None:
        print("No timestamp given, using system time.")
        timestamp = datetime.datetime.now()

    # Insert image to collection
    # img = cv2.imread("orange.png")
    image_bytes = cv2.imencode('.jpg', img)[1].tobytes() # convert to byte string
    db.Visitors.insert_one({"timestamp" : timestamp, 'data' : image_bytes, "user_name" : user})




