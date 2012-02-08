# from application
from gaemvc.methods import View, Action
from gaemvc.handler import BaseController

class HomeController( BaseController ):
    Area = "home"
    
    @Action(redirect="/coverletter/strayboots")
    def index(self, **kwargs):
        self.Template = "portfolio.html"
        return {}

class CoverLetterController( BaseController ):
    Area = "coverletter"
    
    @View()
    def index(self, **kwargs):
        return {}
    
    @View()
    def strayboots(self, **kwargs):
        return {}

class PurpleController( BaseController ):
    Area = "purple"
    
    @View()
    def index(self, **kwargs):
        team = self.load_team("Purple Penetrators")
        return { 'roster' : team.roster }
    
    @View(routes=[
        r"/(?P<key>[A-Za-z0-9-_]+)/$"
    ])
    def view(self, **kwargs):
        return {}
    
    @View(routes=[
        r"/(?P<team>[A-Za-z0-9-_]+)/$"
    ])
    def team(self, **kwargs):
        self.Template = "index.html"
        team_name = self.route.get("team","").replace('-',' ')
        team = self.load_team(team_name)
        return { 'roster' : team.roster }
    
    @View(routes=[
        r"/(?P<key>[A-Za-z0-9-_]+)/$"
    ])
    def player(self, **kwargs):
        return {}
    
    @Action(responseType="json")
    def create_game(self, **kwargs):
        return {}
    
    @Action(responseType="json")
    def add_player(self, **kwargs):
        # from appengine
        from google.appengine.ext import db
        # from application
        from models import Team, Player
        # request arguments
        player_name = kwargs.get("name",None)
        # cast string as db.Key
        team_key    = db.Key(self.session['team_key'])
        # get the player
        player = None
    	if player_name:
            player = Player.get_or_insert(player_name,parent=team_key,name=player_name,team=team_key)
        # return object's db address or null
        return { 'player' : { 'key' : str(player.key()) } } if player else { 'player' : None }
    
    def load_team(self, team_name):
        from models import Team
        team = Team.get_or_insert(team_name,name=team_name)
        self.session['team']     = team.key().name()
        self.session['team_key'] = str(team.key())
        return team
