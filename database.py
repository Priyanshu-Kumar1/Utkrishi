from firebase_admin import db


def store(data, path= "/"):

    ref= db.reference(path)

    ref.set(data)



def get_data(path= "/"):

    ref= db.reference(path)

    return ref.get()



def append_data(data, path= "/"):

    ref= db.reference(path)

    try:

        index = len(ref.get())

    except:

        index = 0

    path = path + f"/{index}"

    store(data, path)


def push(data, path= "/"):

    ref= db.reference(path)

    ref.push().set(data)

    



    



    

if __name__ == "__main__":
    
    

    path= "/"

    print(append_data("hii", path))

    

    

    