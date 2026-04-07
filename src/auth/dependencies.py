from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request, status
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import is_token_blocklisted

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        print(f"Decoded token data: {token_data}")  # Debugging statement
        if token_data is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")

        # Check if the token is blocklisted
        if await is_token_blocklisted(token_data["jti"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is revoked")

        self.verify_token(token_data)
        return token_data


    def verify_token(self, token_data: dict)-> None:
        raise NotImplementedError("Subclasses must implement the verify_token method")

class AccessTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict)-> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token cannot be used for authentication")

class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict)-> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token is not provided")