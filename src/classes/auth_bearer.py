from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

from src.classes.jwt_handler import JwtHandler


class AuthBearer(HTTPBearer):
    """
    A class for handling JWT-based authentication using FastAPI's HTTPBearer.
    """
    def __init__(self, auto_error: bool = True):
        super(AuthBearer, self).__init__(auto_error=auto_error)
        self.jwt_handler_object = JwtHandler()

    def verify_jwt(self, jwtoken: str) -> bool:
        """
        Verifies the validity of a JWT.
        Parameters:
        - jwtoken (str): The JWT to be verified.
        Returns:
        - bool: True if the JWT is valid, False otherwise.
        """
        isTokenValid: bool = False

        try:
            payload = self.jwt_handler_object.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    async def __call__(self, request: Request):
        """
        Overrides the __call__ method to perform JWT authentication.
        Parameters:
        - request (Request): The FastAPI Request object.
        Returns:
        - str: The JWT if authentication is successful.
        Raises:
        - HTTPException: If authentication fails.
        """
        credentials: HTTPAuthorizationCredentials = await super(AuthBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
