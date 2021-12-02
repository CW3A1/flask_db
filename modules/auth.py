from datetime import datetime, timedelta, timezone
from uuid import NAMESPACE_DNS, uuid5

from bcrypt import checkpw, gensalt, hashpw
from fastapi import Request
from jwt import decode, encode

from modules.environment import AUTH_SECRET


def generate_uuid(email):
    identifier = uuid5(NAMESPACE_DNS, email)
    return str(identifier)

def generate_hash(password):
    hashed_password = hashpw(bytes(password, "utf-8"), gensalt())
    return hashed_password.decode("utf-8")

def check_password(password, hashed_password):
    validity = checkpw(bytes(password, "utf-8"), hashed_password.encode("utf-8"))
    return validity

def generate_jwt(identifier):
    token = encode({"uuid": identifier, "exp": datetime.now(tz=timezone.utc) + timedelta(days=1)}, AUTH_SECRET)
    return str(token, "utf-8")

def header_to_identifier(req: Request):
    try:
        token = req.headers["Authorization"]
        decoded = decode(token[7:], AUTH_SECRET)
        identifier = decoded["uuid"]
        return identifier
    except:
        return ""
