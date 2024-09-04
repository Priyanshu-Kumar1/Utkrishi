import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

from database import store



cred = credentials.Certificate("firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    
    "databaseURL": "https://update-20082.firebaseio.com/",
    "storageBucket": "update-20082.appspot.com",
        
        })


def check_user(email):
    try:
        auth.get_user_by_email(email)
    
    except auth.UserNotFoundError:
        return False #returns false if user not found
    
    else:
        return True #returns true if user found
    
def sign_up(email, password):
    
    if check_user(email):
        user = auth.get_user_by_email(email)
        
        
    
    else:
        user = auth.create_user(email= email, password = password)
        store(user.email, user.uid)
        
        
        
    return user
        
    
def get_users():
    users = auth.list_users()
    return users.users



if __name__ == "__main__":
    sign_up("rprem058@gmail.com", "7319656722")

