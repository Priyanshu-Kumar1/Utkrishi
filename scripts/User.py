class User():
    def __init__(self, name=None, email=None, address=None, username=None, user_type=None):
        self.name = name
        self.email = email
        self.username = username
        self.type = user_type
        self.country = None
        self.state = None
        self.city = None
        self.pincode = None
        self.latitude = None
        self.longitude = None
        self.address = None

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def __str__(self):
        return f"User: {self.name}, {self.age}"