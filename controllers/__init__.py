# from application
from gaemvc.methods import controller
# from application.controllers
from controllers.purple import purple
from controllers.apps import smallapp

home = controller("home")

@home.view(redirect_to="/coverletter/")
def index(handler):
	return {}

@home.view()
def coverletter(handler):
    return {}

apps = [home, smallapp, purple]
default_app = home
