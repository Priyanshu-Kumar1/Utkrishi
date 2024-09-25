import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

import json

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(
    cloud_name = "dmpwndgvu", 
    api_key = "854775738857116", 
    api_secret = "BryiOkEv0s5DR7dP8hVQIsG_u3U",
    secure=True
    )

def uploadImage(file, path):

    # Upload the image and get its URL
    # ==============================

    # Upload the image.
    # Set the asset's public ID and allow overwriting the asset with new versions
    path = path.replace(" ", "")
    path = path.replace("&", "")
    url_dict = cloudinary.uploader.upload(file, folder= path, unique_filename = False, overwrite=True)

    # Log the image URL to the console. 
    # Copy this URL in a browser tab to generate the image on the fly.
    return url_dict['url']





from firebase_admin import storage
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

import database as db





def upload_file(file, path):
    
    '''
    bucket = storage.bucket()
    blob = bucket.blob(path)
    blob.upload_from_filename(file)
    return blob.public_url'''
    return uploadImage(file, path)

def get_file(path):
    bucket = storage.bucket()
    blob = bucket.blob(path)
    return blob.public_url


'''
if __name__ == "__main__":
    cred = credentials.Certificate("firebase-sdk.json")

    firebase_admin.initialize_app(cred, {
    
        "databaseURL": "https://update-20082.firebaseio.com/",
        "storageBucket": "update-20082.appspot.com/xNI08LNtmnSK9lLDVUE7HqkHqOj2",
            
            })
    print(get_file("lemon.jpg"))'''