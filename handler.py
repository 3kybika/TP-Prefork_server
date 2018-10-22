# coding=utf-8
import os
from urllib.parse import unquote
from response import ResponseBuilder
from response_config  import ResponseCode, CONTENT_TYPES, ALLOWED_METHODS


class ResponseHandler:
    def __init__(self, root_dir):
        self.root_dir = root_dir
    
    @staticmethod
    def get_url(request):
        url = request.split(b' ')[1].decode()
        return unquote(url.split('?')[0])
    
    @staticmethod
    def get_method(request):
        return request.split(b' ')[0].decode()
    
    @staticmethod
    def get_content_type(path):
        file_type = path.split('.')[-1]
        return CONTENT_TYPES.get(file_type, '')
        
    def handle(self, request):
        method = self.get_method(request)
        path = self.get_url(request)

        if method not in ALLOWED_METHODS:
            return ResponseBuilder(code = ResponseCode.NOT_ALLOWED)

        path = os.path.normpath(self.root_dir + '/' + path)
        if path.find('../') != -1 or os.path.commonprefix([path, self.root_dir]) != self.root_dir:
            return ResponseBuilder(code=ResponseCode.FORBIDDEN)                    
        if os.path.isfile(path):
            return self.create_response(path, method)
        elif os.path.isdir(path):
            path = os.path.join(path, 'index.html')

            if os.path.isfile(path):
                return self.create_response(path, method)
            return ResponseBuilder(code = ResponseCode.FORBIDDEN)

        return ResponseBuilder(code = ResponseCode.NOT_FOUND)

 
    def create_response(self, path, method):
        try: 
            with open(path, 'rb') as f:
                content = f.read()
                return ResponseBuilder(
                    code = ResponseCode.OK,
                    content = content if method != "HEAD" else b'',
                    content_len = len(content),
                    content_type = self.get_content_type(path)
                )
                
        except Exception as e:
            print(e)
            return ResponseBuilder(code = ResponseCode.FORBIDDEN)


