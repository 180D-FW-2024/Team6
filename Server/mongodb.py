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

# Verify name and password combination
def verifyLock(name, password):
    lock = db.Locks.find_one({"name" : name})
    if lock is None:
        print("User does not exist")
        return False
    return lock['password'] == password

# Return door open and unlocked status for given id
def getDoorState(lock_id):
    state = db.Locks.find_one({"id" : lock_id}) 
    if state is None:
        return {'id': "none(lock id does not exist)",
            'door_open' : True, 'door_unlocked' : True}
    return {'id': -1 if state is None else lock_id,
            'door_open' : state['door_open'], 'door_unlocked' : state['door_unlocked']}

def setOpenState(lock_id, door_open):
    db.Locks.update_one({"id": lock_id}, {"$set": {"door_open": door_open}})

def unlockDoor(lock_id):
    db.Locks.update_one({"id": lock_id}, {"$set": {"door_unlocked": True}})

def toggleLock(lock_id):
    #aggregate operator
    db.Locks.update_one({"id": lock_id}, [{ "$set": { "door_unlocked": { "$not": "$door_unlocked" } } }])

# Return cursor of memos for a given id
def getMemos(lock_id):
    memos = db.Memos.find({"lock_id" : lock_id})
    return memos

def addMemo(lock_id, memo, timestamp = None):
    if timestamp == None:
        # print("No timestamp given, using system time.")
        timestamp = datetime.datetime.now()
    db.Memos.insert_one({"timestamp" : timestamp, 'data' : memo, "lock_id" : lock_id})

# Return array of images encoded as base-64 strings(timestamp and data)
def getVisitors(lock_id):
    photos = db.Visitors.find({"lock_id" : lock_id})
    # convert image bytes to string
    # photo['title'] = b64encode(...) does not work, so create separate array
    photoArray = []
    for photo in photos:
        photoArray.append({"timestamp" : photo['timestamp'], "data" : b64encode(photo['data']).decode('utf-8')})
    return photoArray

# Add a photo taken by some user's camera
def addVisitor(lock_id, img, timestamp = None):
    if timestamp == None:
        # print("No timestamp given, using system time.")
        timestamp = datetime.datetime.now()

    # Insert image to collection
    image_bytes = cv2.imencode('.jpg', img)[1].tobytes() # convert to byte string
    db.Visitors.insert_one({"timestamp" : timestamp, 'data' : image_bytes, "lock_id" : lock_id})




