import os

def is_dev():
    return os.environ['SERVER_SOFTWARE'].startswith('Dev')

def is_ajax(handler):
    return handler.request.headers.get("HTTP_X_REQUESTED_WITH",None) == 'xmlhttprequest'
