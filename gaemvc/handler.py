import webapp2
from webapp2_extras import sessions
from gaemvc.methods import View

class BaseController( object ):
    Area      = "shared"
    Template  = None
    AdminOnly = False
    ViewState = {}
    
    def __init__(self, handler):
        self.handler = handler
    
    @property
    def request(self):
        return self.handler.request
    
    @property
    def response(self):
        return self.handler.response
    
    @webapp2.cached_property
    def session(this):
        return this.handler.session_store.get_session()

class Switchboard( webapp2.RequestHandler ):
    VIEW       = 1
    CONTROLLER = 0
    default = BaseController
    
    def __init__(self,*args,**kwargs):
        super(Switchboard, self).__init__(*args, **kwargs)
        self.sites = BaseController.__subclasses__()
    def get(self, tail=""):
        line = tail.split('/')
        for subclass in self.sites:
            if subclass.Area == line[self.CONTROLLER]:
                ctrl = subclass(self)
                if hasattr(subclass,line[self.VIEW]):
                    _View = getattr(subclass,line[self.VIEW])
                    self.response.out.write( _View( ctrl ) )
                else:
                    self.response.out.write( ctrl.index() )
                return
        self.response.out.write( self.default(self).index() )
    def post(self, tail=""):
        self.get(tail)
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
    

