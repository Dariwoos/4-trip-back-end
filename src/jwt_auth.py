import jwt
import datetime

def generate_token(traveler, key):
    print(traveler)
    print(key)
    return jwt.encode({"email":traveler, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},key)

def decode_token(token, key):
    return jwt.decode(token, key, algorithms="HS256")