from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from src.config import Config
import uuid
import logging

password_context = CryptContext(schemes=['bcrypt'])


def hash_password(password: str)->str:
    # Truncate password to 72 bytes as required by bcrypt
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        password = password_bytes.decode('utf-8', errors='replace')
    hash = password_context.hash(password)
    return hash

def verify_password(password: str, password_hash: str)-> bool:
    return password_context.verify(password, password_hash)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(seconds=Config.ACCESS_TOKEN_EXPIRY), refresh: bool = False)-> str:
    now = datetime.now(timezone.utc)
    payload = {
        'user': data,
        'iat': now,
        'exp': now + expires_delta,
        'jti': str(uuid.uuid4()),
        'refresh': refresh,
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token

def decode_token(token: str)->dict:
    try:
        token_data = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
            options={"require": ["exp", "iat", "jti"]},
            leeway=10
        )
        return token_data
    except jwt.ExpiredSignatureError:
        logging.error("Token expired")
    except jwt.ImmatureSignatureError:
        logging.error("Token not yet valid (iat)")
    except jwt.InvalidTokenError as e:
        logging.error(f"Token error: {e}")
    return None