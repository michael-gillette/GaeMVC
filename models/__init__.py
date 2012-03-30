import time
import markdown
from google.appengine.ext import db
from gaemvc.properties import HashProperty

class Writer( db.Model ):
    nickname = db.StringProperty()
    password = HashProperty()

class Entry( db.Model ):
    author  = db.ReferenceProperty(Writer, collection_name="entries")
    title   = db.StringProperty()
    content = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    edited  = db.DateTimeProperty(auto_now=True)
    
    @property
    def characters(self):
        return len(self.content)
    
    @property
    def words(self):
        return self.content.count(' ')
    
    @property
    def html(self):
        return markdown.markdown(self.content)
    
    @property
    def isodate(self):
        return str(self.edited)
