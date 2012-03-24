import webapp2
from webapp2_extras import sessions
from gaemvc.methods import controller

shared = controller("shared")

@shared.view()
def index(request, response): return {}

@shared.view()
def http404(request, response): return {}

class Switchboard( webapp2.RequestHandler ):
    controllers = []
    default     = shared
    
    def __init__(self,*args,**kwargs):
        super(Switchboard, self).__init__(*args, **kwargs)
    
    def get(self, tail=""):
        line = tail.split('/')
        
        if not line[0]:
            view = self.default.all['index']
        elif line[0] in self.default.all:
            view = self.default.all[line[0]]
        else:
            for ctrl in self.controllers:
                if ctrl.area == line[0]:
                    view = ctrl.all.get(line[1],ctrl.all['index']);break
        self.response.out.write( view(self) )
    
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
    

