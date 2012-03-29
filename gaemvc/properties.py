import hashlib

class HashProperty( db.Property ):
    data_type = str
    
    def __init__(self, *args, **kwargs):
        try:
            self._fn = kwargs['method']
            del kwargs['method']
        except KeyError as ke:
            self._fn = hashlib.md5
        super(HashProperty,self).__init__(*args, **kwargs)
    
    def get_value_for_datastore(self, model_instance):
        return self(model_instance.password)
    
    def make_value_from_datastore(self, value):
        return value
    
    def __call__(self, value):
        ret = self._fn(value)
        try:
            return ret.hexdigest()
        except:
            return ret
