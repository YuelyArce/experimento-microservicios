from jwt import encode
from os import getenv
from datetime import datetime, timedelta


def write_token(data: dict):
    """Funciòn que crea jwt
    """
    
    now = datetime.utcnow()
    exp = now + timedelta(hours=1)

    datos_encode = {
        'role': data.get('role'),
        'usuario': data.get('usuario'),
        'exp': exp
        }
    token = encode(payload=datos_encode, key=getenv('SECRET'), algorithm='HS256')

    return token