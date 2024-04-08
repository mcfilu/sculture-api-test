import hashlib

def hashed_token(email, salt="1325143SomethingTotest21521"):
    password_hash = hashlib.sha256((email + salt).encode('utf-8')).hexdigest()
    return password_hash