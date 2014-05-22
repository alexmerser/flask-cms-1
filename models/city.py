from lib.model import Model, Dao

class City(Model):
        
    def __init__(self, _dict):
        Model.__init__(self, _dict)
        
        self.city = _dict['city']
        self.province = _dict['province']
        self.country = _dict['country']
        
    def __repr__(self):
        return '<City %r>' % ('Model')

class CityDao(Dao):
    def __init__(self):
        """Arguments:
            collection --- string the name of the collection
        """
        Dao.__init__(self, City)
        self.collection = 'cities'
        
if __name__ == '__main__':
    pass
