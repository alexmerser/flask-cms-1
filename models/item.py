from lib.model import Model, Dao

# Enum PropertyType
class PropertyType:
    NoneType = 0,
    Room = 1,
    House = 2,
    Apartment = 3,
    Commercial = 4

class Item(Model):
    
    def __init__(self, _dict):
        Model.__init__(self, _dict)

        # Basic properties
        self.title = _dict['title']
        self.description = _dict['description']
        self.price = _dict['price']
        self.created = _dict['created']

        # Additional properties
        self.email = _dict['email']
        self.phone = _dict['phone']
        self.property_type = _dict['property_type']

class ItemDao(Dao):
    def __init__(self):
        Dao.__init__(self, Item)
        
        self.collection = 'items'
    

class ItemPicture(Model):
    def __init__(self, _dict):
        Model.__init__(self, _dict)
        self.fpath = _dict['fpath']
        self.item_id = _dict['item_id']


class ItemPictureDao(Dao):
    def __init__(self):
        Dao.__init__(self, ItemPicture)
        
        self.collection = 'item_pictures'
        

if __name__ == '__main__':
    pass
