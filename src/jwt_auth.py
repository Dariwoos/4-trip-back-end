import jwt
import datetime

def generate_token(email,rol,id,key):
    print(rol)
    print(key)
    return jwt.encode({"email":email,"rol":rol, "id":id, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},key)

def decode_token(token, key):
    return jwt.decode(token, key, algorithms="HS256")