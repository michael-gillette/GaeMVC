# from appengine
from webapp2_extras import json
from google.appengine.ext import db
# from application
from gaemvc.methods import View, Action
from gaemvc.handler import BaseController

class PurpleController( BaseController ):
    Area = "purple"
    
    ##
    # ==|== populate pages with data
    ##
    
    @View()
    def index(self, **kwargs):
        team = self.load_team("Purple Penetrators")
        return { 'roster' : team.roster }
    
    @View(routes=[
        r"/(?P<team>[A-Za-z0-9-_]+)/$"
    ])
    def team(self, **kwargs):
        self.Template = "index.html"
        team_name = self.route.get("team","").replace('-',' ')
        team = self.load_team(team_name)
        return { 'roster' : team.roster }
    
    ##
    # ==|== AJAX api for javascript =====
    ##
    
    @Action(responseType="json")
    def cleanup(self, **kwargs):
        from models.stats import Game
        
        game = db.get(self.session['game'])
        
        if not game.standings:
            db.delete(game)
        
        return {}
    
    @Action(responseType="json")
    def save_record(self, **kwargs):
        from models.stats import Player, Record
        # prepare
        player   = kwargs.get("player",None)
        raw_data = kwargs.get("data","{}")
        data     = json.decode(raw_data)
        
        if player and data:
            # create a record
            record = Record(player=db.Key(player),game=db.Key(self.session['game']))
            record.import_dict(data)
            record.put()
        return { "success" : False }
    
    @Action(responseType="json")
    def add_player(self, **kwargs):
        from google.appengine.ext import db
        from models.stats import Team, Player
        
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
    
    def load_team(self, team_name=None):
        from models.stats import Team
        team = Team.get_or_insert(team_name,name=team_name)
        self.session['team']     = team.key().name()
        self.session['team_key'] = str(team.key())
        self.session['game']     = self.the_game
        return team
    
    @property
    def the_game(self):
        if 'game' not in self.session:
            from models.stats import Game
            game = Game(team=db.Key(self.session['team_key']))
            game.put()
            self.session['game'] = str(game.key())
        return self.session['game']
    