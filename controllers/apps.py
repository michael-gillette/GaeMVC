# from appengine
from webapp2_extras import json
from google.appengine.ext import db
# from application
from gaemvc.methods import View, Action
from gaemvc.handler import BaseController

class AppsController( BaseController ):
    Area = "app"
    
    ## EEE application
    @View()
    def eee(self, **kwargs):
        return {}
    
    @View()
    def craigslist(self, **kwargs):
        return {}
    
    ## Css3 Button generator View + Action
    @View()
    def cssbutton(self, **kwargs):
        return {}
    
    @Action(responseType="json")
    def generatecssbutton(self, **kwargs):
        return {}
