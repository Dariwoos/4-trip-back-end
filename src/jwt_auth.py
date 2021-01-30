import jwt
import datetime

def generate_token(traveler, key):
    print(traveler)
    print(key)
    return jwt.encode({"traveler":traveler, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},key)

def decode_token():
    return jwt.decode(token, key, algorithms="HS256")