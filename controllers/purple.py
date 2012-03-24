# from appengine
from webapp2_extras import json
from google.appengine.ext import db
# from application
from models.stats import Team, Player
from gaemvc.methods import controller

def load_game(handler):
    if 'game' not in handler.session:
        from models.stats import Game
        game = Game(team=db.Key(handler.session['team_key']))
        game.put()
        handler.session['game'] = str(game.key())
    return handler.session['game']

def load_team(handler, team_name):
    from models.stats import Team
    team = Team.get_or_insert(team_name,name=team_name)
    handler.session['team']     = team.key().name()
    handler.session['team_key'] = str(team.key())
    handler.session['game']     = load_game(handler)
    return team

purple = controller("purple")

@purple.view()
def index(handler, **kwargs):
    team = load_team(handler, "Purple Penetrators")
    return { "roster" : team.roster }

@purple.view(routes=[r"/(?P<team>[A-Za-z0-9-_]+)/$"])
def team(handler, params, route):
    team_name = route.get("team","").replace("-"," ")
    team      =  load_team(handler, team_name)
    return { 'roster' : team.roster, '__template' : 'index.html' }

@purple.view(response_type="json")
def cleanup(handler, **kwargs):
    from models.stats import Game
    
    game = db.get(handler.session['game'])
    
    if not game.standings:
        db.delete(game)
    
    return {}

@purple.view(response_type="json")
def save_record(handler, params, **kwargs):
    from models.stats import Player, Record
    
    player   = params.get("player", "")
    raw_data = params.get("data","{}")
    data     = json.decode(raw_data)
    
    if player and data:
        record = Record(player=db.Key(player),game=db.Key(handler.session['game']))
        record.import_dict(data)
        record.put()
        return { "success" : True }
    
    return { "success" : False }
    
@purple.view(response_type="json")
def add_player(handler, params, **kwargs):
    from google.appengine.ext import db
    from models.stats import Team, Player
    
    # request arguments
    player_name = params.get("name",None)
    
    # cast string as db.Key
    team_key    = db.Key(handler.session['team_key'])
    
    # get the player
    player = None
    if player_name:
        player = Player.get_or_insert(player_name,parent=team_key,name=player_name,team=team_key)
    
    # return object's db address or null
    return { 'player' : { 'key' : str(player.key()) } } if player else { 'player' : None }

    