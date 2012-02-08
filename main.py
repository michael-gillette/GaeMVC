import webapp2
# from gaemvc
from gaemvc.utils import is_dev
from gaemvc.handler import Switchboard
# from application
from controllers import *

class Operator(Switchboard):
    default = HomeController

# for session support
config = webapp2.Config()
config['webapp2_extras.sessions'] = {
	'secret_key' : '295a512ae598c015edd690abf03ece98',
}

app = webapp2.WSGIApplication([
    (r'/(.*)',Operator)
], debug=is_dev(), config=config)
