# from appengine
from google.appengine.ext import db

class Team( db.Model ):
    name = db.StringProperty()

class Player( db.Model ):
    name = db.StringProperty()
    team = db.ReferenceProperty(Team,collection_name="roster")

class Game( db.Model ):
    title = db.StringProperty(default="Untitled")
    team  = db.ReferenceProperty(Team,collection_name="games")

class Record( db.Model ):
    game = db.ReferenceProperty(Game,collection_name="standings")
    player = db.ReferenceProperty(Player,collection_name="records")
    fgm  = db.IntegerProperty()
    fga  = db.IntegerProperty()
    tgm = db.IntegerProperty()
    tga = db.IntegerProperty()
    ftm  = db.IntegerProperty()
    fta  = db.IntegerProperty()
    reb  = db.IntegerProperty()
    ast  = db.IntegerProperty()
    stl  = db.IntegerProperty()
    blk  = db.IntegerProperty()
    to   = db.IntegerProperty()
    
    @property
    def points(self):
        return (self.fgm * 2) + (self.tgm * 3) + (self.ftm * 1)
    
    @property
    def efficiency(self):
        return self.points + self.reb + self.ast + self.stl + self.blk - ((self.fga+self.tga)-(self.fgm+self.tgm)) - (self.fta-self.ftm) - self.to
    
    def import_dict(self, data={}):
        for k,v in data.items():
            if k in ['fgm','fga','tgm','tga','ftm','fta','reb','ast','stl','blk','to']:
                self.__setattr__(k,v)
