import bcrypt as bc

def get_hashed_password(plain_text_password):
    return bc.hashpw(plain_text_password.encode("utf8"), bc.gensalt())

def check_password(plain_text_password, hashed_password):
    return bc.checkpw(plain_text_password.encode("utf8"), hashed_password)