from jose import jwt
import time


class JwtHandler:
    def __init__(self):
        self.access_token_expire_minutes = 30 
        self.jwt_secret_key = "58b28a43900e176f3148054ea30d"
        self.algorith = "HS256"
    def token_response(self, token: str):
        return {
            'access token' : token
        }

    def signJWT(self, userID : str):
        expiration_time = int(time.time()) + self.access_token_expire_minutes * 60
        payload = {
            "userID" : userID,
            "expirity" : expiration_time
        }
        token = jwt.encode(payload, key= self.jwt_secret_key, algorithm= self.algorith)
        return self.token_response(token)

    def decodeJWT(self, token: str):
        try:
            decode_token = jwt.decode(token, key= self.jwt_secret_key, algorithms= self.algorith)
            return decode_token if decode_token['expirity'] >= time.time() else None
        except:
            return {}