import webapp2
from webapp2_extras import sessions
from gaemvc.methods import View

class BaseController( object ):
    Area      = "shared"
    Template  = None
    Theme     = None
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
    def session(self):
        return self.handler.session_store.get_session()

class Switchboard( webapp2.RequestHandler ):
    VIEW       = 1
    CONTROLLER = 0
    default = BaseController
    
    def __init__(self,*args,**kwargs):
        super(Switchboard, self).__init__(*args, **kwargs)
        self.sites = BaseController.__subclasses__()
    def get(self, tail=""):
        import logging
        line = tail.split('/')
        
        # check against default controller
        if hasattr(self.default, line[0]):
            return self.response.out.write( getattr(self.default, line[0])(self.default(self)) )            
            
        
        # view does not belong to default controller
        for subclass in self.sites:
            if subclass.Area == line[self.CONTROLLER]:
                ctrl = subclass(self)
                if hasattr(subclass,line[self.VIEW]):
                    _View = getattr(subclass,line[self.VIEW])
                    return self.response.out.write( _View( ctrl ) )
                
                return self.response.out.write( ctrl.index() )
        
        # no dice: respond with index
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
    

