# from application
from gaemvc.methods import View, Action
from gaemvc.handler import BaseController

class CoverLetterController( BaseController ):
    Area = "coverletter"
    
    @View()
    def index(self, **kwargs):
        return {}
    
    @View()
    def strayboots(self, **kwargs):
        return {}
