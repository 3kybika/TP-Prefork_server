# coding=utf-8
import config

from datetime import datetime 
from response_config import HTTP_VERSION, SERVER_NAME, RESPONSE_STATUS, HTTP_DATE_FORMAT, ResponseCode,CONTENT_TYPES
from enum import Enum

class ResponseBuilder:
    def __init__(self, code, content_len=0, content_type='', content=b''):
        self.code = code
        self.content_length = content_len
        self.content_type = content_type
        self.body = content

    def build_response(self):
        if self.code is ResponseCode.OK:
            return '''\
HTTP/{http_ver} {http_status}\r\n\
Server: {server_name}\r\n\
Date: {date}\r\n\
Connection: Close\r\n\
Content-Length: {content_length}\r\n\
Content-Type: {content_type}\r\n\r\n\
'''.format(
            http_ver=HTTP_VERSION,
            http_status=RESPONSE_STATUS[self.code.value],
            server_name=SERVER_NAME,
            date=self.date_now(),
            content_length=self.content_length,
            content_type=self.content_type
        ).encode() + self.body
        else:
            return '''\
HTTP/{http_ver} {http_status}\r\n\
Server: {server_name}\r\n\
Date: {date}\r\n\
Connection: Closed\r\n\r\n\
'''.format(
            http_ver=HTTP_VERSION,
            http_status=RESPONSE_STATUS[self.code.value],
            server_name=SERVER_NAME,
            date=self.date_now()
        ).encode()



    @staticmethod
    def date_now():
        return datetime.utcnow().strftime(HTTP_DATE_FORMAT)