# from application
from gaemvc.methods import View, Action
from gaemvc.handler import BaseController
# from application.controllers
from controllers.portfolio import *
from controllers.purple import *
from controllers.apps import *

class HomeController( BaseController ):
    Area = "home"
    
    @Action(redirect="/coverletter/")
    def index(self, **kwargs):
        self.Template = "portfolio.html"
        return {}
