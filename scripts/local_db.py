import json


def store(uid, data):
    with open("user_db.json", "r") as file:
        file_data = json.load(file)


    for k, v in data.items():
        file_data[uid][k] = v
    
    with open("user_db.json", "w") as file:
        json.dump(file_data, file)


def get_data():
    try:
        with open("user_db.json", "r") as file:
            data = json.load(file)
        
        return data
    except:
        return None

def get_email(uid):
    with open("user_db.json", "r") as file:
        data = json.load(file)
    
    for email, id in data.items():
        if id == uid:
            return email
    
    return None

def store_login(data):
    data = {
        "auto_login": True,
        "auto_login_uid": data['uid'],
        data['uid']: data
    }
    with open("user_db.json", "w") as file:
        json.dump(data, file)


def get_auto_login_data():
    try:
        with open("user_db.json", "r") as file:
            data = json.load(file)

    except:
        return None

    if data["auto_login"]:
        uid = data["auto_login_uid"]
        print(data[uid])
        return data[data["auto_login_uid"]]

def check_login(email, password):
    with open("user_db.json", "r") as file:
        data = json.load(file)
    
    return data.get(email, None) == password


if __name__ == "__main__":
    store_login("rprem058@gmail.com")