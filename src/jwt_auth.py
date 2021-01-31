import jwt
import datetime

def generate_token(traveler,rol, key):
    print(rol)
    print(key)
    return jwt.encode({"email":traveler,"rol":traveler, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},key)

def decode_token(token, key):
    return jwt.decode(token, key, algorithms="HS256")