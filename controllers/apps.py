# from appengine
from webapp2_extras import json
from google.appengine.ext import db
# from application
from gaemvc.methods import controller

smallapp = controller("app")

@smallapp.view()
def index(handler): return {}

@smallapp.view()
def craigslist(handler): return {}

@smallapp.view()
def cssbutton(handler): return {}

@smallapp.view(response_type="json")
def generatecssbutton(handler): return {}
