from jwt import decode
from os import getenv
from datetime import datetime, timedelta
from jwt import exceptions



def validate_token(token):
    try:     
        token_data = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        return token_data, 200
    except exceptions.DecodeError:
        response =  {"message": "Invalid Token"}
        status_code = 401
        return response, status_code
    except exceptions.ExpiredSignatureError:
        response =  {"message": "Token Expired"}
        status_code = 401 
        return response, status_code