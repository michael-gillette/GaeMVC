import os

def is_dev():
    return os.environ['SERVER_SOFTWARE'].startswith('Dev')

