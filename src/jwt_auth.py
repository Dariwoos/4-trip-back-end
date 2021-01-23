import jwt
import datetime

def generate_token(traveler, key):
    return jwt.encode({"traveler":traveler, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},key)

def decode_token():
    pass