from datetime import datetime
import jwt


class JWT:
    def __init__(self):
        self.__secret = "its a secret Johny"
        self.__algorithm = "HS256"

    def create_token(self, user):
        payload = {"username": user}
        token = jwt.encode(payload, self.__secret)
        return token.decode('utf-8')

    def verify_token(self, token):
        try:
            jwt.decode(token, self.__secret, algorithms=[self.__algorithm])
            return True
        except:
            return False


auth = JWT()
