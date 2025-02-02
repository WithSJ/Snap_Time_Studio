from math import dist
from app.firebase.config import firebase

database = firebase.database()

def CreateNewUser(localId,fullname="",username="",userData=""):
    username = username.lower()
    userInfo = firebase.auth().get_account_info(userData["idToken"])
    database.child("Users").child(localId).set(
        {   "Fullname":fullname,
            "Username": username,
            "UserData": userData,
            "UserInfo": userInfo
        })

def GetData(localId):
    data = database.child("Users").child(localId).get()
    data = dict(data.val())
    return data

def Update_Fullname_Username(localId,newFullname=None,newUsername=None):
    newUsername = newUsername.lower()
    data = database.child("Users").child(localId).get()
    data = dict(data.val())
    
    if newFullname != None:
        data["Fullname"]= newFullname
    if newUsername != None:
        data["Username"] = newUsername
    
    database.child("Users").child(localId).update(data)

def UploadPhotosData_onFirebase(id,title,dateTime,image,imageTag=None):
    imageName = str(title).replace(" ","") + str(id)
    database.child("PhotosData").child(id).set(
        {   "Id" : id,
            "Title" : title,
            "DateTime" : dateTime,
            "ImageName" : imageName,
            "ImageTag" : imageTag
        })

def UploadVideosData_onFirebase(id,title,dateTime,videoUrl,videoTag=None):
    database.child("VideosData").child(id).set(
        {   "Id" : id,
            "Title" : title,
            "DateTime" : dateTime,
            "VideoUrl" : videoUrl,
            "videoTag" : videoTag
        })

def NewBookingOrder(localId:str,orderTimeStamp:str,orderData: dict)-> None:
    database.child(
        "BookingOrders").child(orderTimeStamp).set(orderData)
    database.child(
        "MyBookingOrders").child(
            localId).child(
                orderTimeStamp).set(orderData)

def GetMyBookingOrders(localId):
    data = database.child("MyBookingOrders").child(localId).get()
    dataOrderKey = list(data.val())
    dataOrder = dict(data.val())
    return [dataOrderKey,dataOrder]

def GetAllOrders():
    allOrders = database.child("BookingOrders").get().val()
    allOrdersKey = list(allOrders)
    allOrders = dict(allOrders)
    return allOrdersKey,allOrders
