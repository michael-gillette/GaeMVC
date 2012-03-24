from google.appengine.ext import db

class BreadBoard( db.Model ):
    pass

class TwoPoints( db.Model ):
    pass

class Wire( db.Model ):
    pass

class LED( db.Model ):
    cathode = db.ReferenceProperty()
    anode   = db.ReferenceProperty()

class IntegratedCircuit( db.Model ):
    pass

class IC555( IntegratedCircuit ):
    pass
