from enum import Enum

class ResponseCode(Enum):
    OK = 200
    FORBIDDEN = 403
    NOT_FOUND = 404
    NOT_ALLOWED = 405

RESPONSE_STATUS = {
    200: "200 OK",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
}

CONTENT_TYPES = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'swf': 'application/x-shockwave-flash'
}

HTTP_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

ALLOWED_METHODS = ["GET", "HEAD"]

HTTP_VERSION = '1.1'
SERVER_NAME = 'HttpServer'