import bcrypt

def encrypted_pass(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
    return hashed

def compare_pass(password, hashed_password):
    print(password)
    print(hashed_password)
    if (bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))):
        return True
    else:
        return False