# Database API
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from base64 import b64encode
from bson import json_util
from bson import ObjectId
import json
import time
import datetime
import cv2
import numpy as np
import os

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
def verifyLock(username, password):
    lock = db.Locks.find_one({"name" : username})
    if lock is None:
        print("User does not exist")
        return False
    return lock['password'] == password

def addLock(username, password, lock_id):
    lock = db.Locks.find_one({"name" : username})
    if lock is not None:
        print("User already exists")
        return False
    db.Locks.insert_one({"name" : username, "password" : password, "id" : lock_id, "door_open" : False, "door_unlocked" : False})
    return True

# Return door open and unlocked status for given id
def getDoorState(lock_id):
    state = db.Locks.find_one({"id" : lock_id}) 
    if state is None:
        return {'id': "none(lock id does not exist)",
            'door_open' : True, 'door_unlocked' : True}
    return {'id': -1 if state is None else lock_id,
            'door_open' : state['door_open'], 'door_unlocked' : state['door_unlocked']}

def getLockid(username):
    lock = db.Locks.find_one({"name" : username})
    return lock['id']

def setOpenState(lock_id, door_open):
    db.Locks.update_one({"id": lock_id}, {"$set": {"door_open": door_open}})

def unlockDoor(lock_id):
    db.Locks.update_one({"id": lock_id}, {"$set": {"door_unlocked": True}})

def lockDoor(lock_id):
    db.Locks.update_one({"id": lock_id}, {"$set": {"door_unlocked": False}})

def toggleLock(lock_id, door_unlocked):
    # aggregate operator (does not work)
    # db.Locks.update_one({"id": lock_id}, [{ "$set": { "door_unlocked": { "$not": "$door_unlocked" } } }])
     db.Locks.update_one({"id": lock_id}, {"$set": {"door_unlocked": door_unlocked}})

# Return cursor of memos for a given id
def getMemos(lock_id):
    cursor = db.Memos.find({"lock_id" : lock_id})
    memos = []
    for memo in cursor:
        memos.append({"timestamp" : memo['timestamp'], "data": memo['data'],
                      "id" : json.loads(json_util.dumps(memo['_id']))["$oid"]})
    return memos

def addMemo(lock_id, memo, timestamp = None):
    if timestamp == None:
        # print("No timestamp given, using system time.")
        timestamp = datetime.datetime.now()
    db.Memos.insert_one({"timestamp" : timestamp, 'data' : memo, "lock_id" : lock_id})

# Delete memo with the given object id
def deleteMemo(memo_id):
    # db.Visitors.delete_many({"_id" : {"$in" : [ ObjectId(id) for id in ids ] }})
    db.Memos.delete_one({"_id" : ObjectId(memo_id)})

# Return array of images encoded as base-64 strings(timestamp and data)
def getVisitors(lock_id):
    photos = db.Visitors.find({"lock_id" : lock_id})
    # convert image bytes to string
    # photo['title'] = b64encode(...) does not work, so create separate array
    photoArray = []
    for photo in photos:
        photoArray.append({"timestamp" : photo['timestamp'], "data" : b64encode(photo['data']).decode('utf-8'),
                           "id" : json.loads(json_util.dumps(photo['_id']))["$oid"]})
    return photoArray

# Add a photo taken by some user's camera
def addVisitor(lock_id, img, timestamp = None):
    if timestamp == None:
        # print("No timestamp given, using system time.")
        timestamp = datetime.datetime.now()

    # Insert image to collection
    image_bytes = cv2.imencode('.jpg', img)[1].tobytes() # convert to byte string
    db.Visitors.insert_one({"timestamp" : timestamp, 'data' : image_bytes, "lock_id" : lock_id})

# Delete visitor images with the given object id
def deleteVisitor(image_id):
    # db.Visitors.delete_many({"_id" : {"$in" : [ ObjectId(id) for id in ids ] }})
    db.Visitors.delete_one({"_id" : ObjectId(image_id)})

def getResidents(lock_id):
    residentArray = []
    residents = db.Residents.aggregate([{"$match" :{ "lock_id" :lock_id}},
        { "$group" : { "_id" : "$name", "images": { "$push": {"data":"$data", "_id":"$_id"} } } }
    ]) # SELECT name, Residents.data AS images GROUP BY Residents.name
    for resident in residents:
        images = [{"data" : b64encode(img['data']).decode('utf-8'), 
                   "id":json.loads(json_util.dumps(img['_id']))["$oid"]} for img in resident['images']]
        residentArray.append({"name":resident["_id"], "images" : images})
    return residentArray

# Add a resident with the given visitor image ids
def addResident(lock_id, name, ids):
    imgArray = []
    imgs = db.Visitors.find({"lock_id" : lock_id, "_id" : {"$in" : [ ObjectId(id) for id in ids ] }})
    for img in imgs:
        imgArray.append({"lock_id" : lock_id, "name" : name, "data": img["data"]})
    db.Residents.insert_many(imgArray)


# Delete resident images of given lock_id with given name
def deleteResident(name, lock_id):
    db.Residents.delete_many({"name" : name, "lock_id" : lock_id})


def uploadKnownFace(lock_id, img, name):
    image_bytes = cv2.imencode('.jpg', img)[1].tobytes() # convert to byte string
    db.Residents.insert_one({"lock_id" : lock_id, "data": image_bytes, "name": name})

# Save known faces (residents) locally
def downloadKnownFaces(lock_id, path):
    residents = db.Residents.find({"lock_id" : lock_id})
    for resident in residents:
        name_path = path + "/"+str(lock_id) + "/" + resident["name"]
        if not os.path.exists(name_path):
            os.makedirs(name_path)
        img_np = np.frombuffer(resident["data"], np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR) # deepface uses BGR space
        cv2.imwrite(name_path + "/" + json.loads(json_util.dumps(resident['_id']))["$oid"] + ".jpg", img)