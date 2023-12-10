from jose import jwt
import time


class JwtHandler:
    """
    A class for handling JSON Web Tokens (JWT) creation, signing, and decoding.
    """
    def __init__(self):
        self.access_token_expire_minutes = 30 
        self.jwt_secret_key = "58b28a43900e176f3148054ea30d"
        self.algorith = "HS256"
    def token_response(self, token: str) -> dict:
        """
        Returns a dictionary containing the access token.
        Parameters:
        - token (str): The access token.
        Returns:
        - dict: A dictionary containing the access token.
        """
        return {
            'access token' : token
        }

    def signJWT(self, userID : str) -> dict:
        """
        Signs a JWT with the specified user ID.
        Parameters:
        - user_id (str): The user ID to be included in the JWT payload.
        Returns:
        - dict: A dictionary containing the access token.
        """
        expiration_time = int(time.time()) + self.access_token_expire_minutes * 60
        payload = {
            "userID" : userID,
            "expirity" : expiration_time
        }
        token = jwt.encode(payload, key= self.jwt_secret_key, algorithm= self.algorith)
        return self.token_response(token)

    def decodeJWT(self, token: str) -> dict:
        """
        Decodes a JWT and returns the payload if valid and not expired.
        Parameters:
        - token (str): The JWT to be decoded.
        Returns:
        - dict: The payload of the decoded JWT if valid and not expired.
        """
        try:
            decode_token = jwt.decode(token, key= self.jwt_secret_key, algorithms= self.algorith)
            return decode_token if decode_token['expirity'] >= time.time() else None
        except:
            return {}