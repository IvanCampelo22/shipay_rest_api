import os, jwt 
from fastapi import HTTPException
from fastapi import Request, HTTPException
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings



def decodeJWT(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        return payload
    except InvalidTokenError:
        return None


class JWTBearerUser(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearerUser, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerUser, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

jwt_bearer = JWTBearerUser()