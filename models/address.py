from lib.model import Model, Dao

class Address(Model):
    def __init__(self, _dict):
        Model.__init__(self, _dict)

        self.unit = _dict['unit']
        self.street = _dict['street']
        self.postcode = _dict['postcode']

        # associate fields
        self.city_id = _dict['city_id']

    def __repr__(self):
        return '<Address %r>' % ('Model')
    
class AddressDao(Dao):
    def __init__(self):
        """Arguments:
            collection --- string the name of the collection
        """
        Dao.__init__(self, Address)
        self.collection = 'addresses'
        
        # associates { field name : collection name }
        self.ref_collections = {'city':'cities'}
        



if __name__ == '__main__':
    pass
    
