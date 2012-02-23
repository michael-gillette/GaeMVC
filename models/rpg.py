# from appengine
from google.appengine.ext import db

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
