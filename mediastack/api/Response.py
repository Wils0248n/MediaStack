from enum import Enum
from typing import Tuple, Dict

class ResponseType(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

class Response():
    def __init__(self, response_type: ResponseType, data = '', message: str = ''):
        self.response_type = response_type
        self.data = data
        self.message = message

    def getResponse(self) -> Tuple[Dict, int]:
        return {'message':self.message, 'data':self.data}, self.response_type.value
    