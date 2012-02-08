# from appengine
from google.appengine.ext import db

class Team( db.Model ):
    name = db.StringProperty()

class Player( db.Model ):
    name = db.StringProperty()
    team = db.ReferenceProperty(Team,collection_name="roster")

class Game( db.Model ):
    team = db.ReferenceProperty(Team,collection_name="games")

class Record( db.Model ):
    game = db.ReferenceProperty(Game,collection_name="standings")
    player = db.ReferenceProperty(Player,collection_name="records")
    fgm  = db.IntegerProperty()
    fga  = db.IntegerProperty()
    tfgm = db.IntegerProperty()
    tfga = db.IntegerProperty()
    ftm  = db.IntegerProperty()
    fta  = db.IntegerProperty()
    reb  = db.IntegerProperty()
    ast  = db.IntegerProperty()
    stl  = db.IntegerProperty()
    blk  = db.IntegerProperty()
    to   = db.IntegerProperty()
    
    @property
    def points(self):
        return (self.fgm * 2) + (self.tfgm * 3) + (self.ftm * 1)
    
    @property
    def efficiency(self):
        return self.points + self.reb + self.ast + self.stl + self.blk - (self.fga-self.fgm) - (self.fta-self.ftm) - self.to

###
##  RPG Models
###

class Officer( db.Model ):
    # equipment slots
    offense_json = db.TextProperty(default="{}")
    defense_json = db.TextProperty(default="{}")
    sentry_json  = db.TextProperty(default="{}")
    spy_json     = db.TextProperty(default="{}")
    
    # equipment setters
    def update_equipment(self,latest_equipment,attr="offense_json",persist=True):
        # from appengine
        from webapp2_extras import json
        
        # load json
        latest    = json.decode(latest_equipment)
        equipment = json.decode(self.__getattribute__(attr))
        
        # apply changes to container
        for k,v in latest.items():
            equipment[k] = equipment[k] + v
            
        # set the changes
        self.__setattr__(attr,json.encode(equipment))
        
        # persist changes if required
        if persist: self.put()
        
        # return dict of all objects
        return equipment
