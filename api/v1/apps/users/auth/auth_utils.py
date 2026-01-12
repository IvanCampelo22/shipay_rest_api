from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings
from jwt.exceptions import InvalidTokenError
from fastapi.exceptions import HTTPException
from fastapi import Request
from loguru import logger
import base64
import json
import jwt

def decodeJWT(jwtoken: str):
    jwt_options = {
        'verify_signature': False,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }

    try:
        payload = json.loads(json.dumps(jwt.decode(jwt=jwtoken,
                              key=settings.JWT_SECRET_KEY,
                              algorithms=settings.ALGORITHM,
                              options=jwt_options)))
                    
        print(payload)
        return payload
    except InvalidTokenError as e:
        logger.error(f'{e}')
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
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
    

jwt_bearer = JWTBearer()


def format_jwt(token):
    token_decode = token.split(".")[1]

    padding = '=' * (4 - len(token_decode) % 4)
    token_decode += padding

    decoded_bytes = base64.urlsafe_b64decode(token_decode)
    decoded_str = decoded_bytes.decode('utf-8')

    decoded_payload = json.loads(decoded_str)

    return decoded_payload