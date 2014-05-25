from models.item import ItemDao
from lib.validator import Validator
from lib.form import Form, Mode
from services import Service
from services.address import CityService, AddressService
from models.item import PropertyType

from bson.objectid import ObjectId

import time

class ItemService(Service):
    def __init__(self):
        self.dao = ItemDao()
        #self.item_picture_dao = ItemPictureDao()


    '''
    def get_default_picture_path(self, item):
        """Arguments:
            item -- must be Model class
        """
        company = self.company_dao.find_one({'_id':item.company['_id']})
        pic = self.item_picture_dao.find_one({'item_ref': DBRef('items',item._id)})
        
        if pic is None:
            picture_serv = ItemPictureService(company.name, item._id)
            return picture_serv.builtin_path
        else:
            return pic.fpath
    '''
    def get_item(self, sid):
        """
        Argument:
            sid -- string type
        """
        if sid != '':
            oid = ObjectId(sid)
            item = self.dao.find_one({'_id':oid})
            return {'id':str(item['_id']),
                    'title':item['title'], 
                    'description':item['description'], 
                    'price':item['price'],
                    'created':item['created'],
                    'property_type':item['property_type']}
        else:
            return None
        
    def get_items(self, query={}):
        """ Get the items for rendering the html
        """
        items = self.dao.find(query)
        
        if items is not None:
            _items = []
            for item in items:
                _items.append({'id':str(item['_id']),
                    'title':item['title'], 
                    'description':item['description'], 
                    'price':item['price'],
                    'created':item['created'],
                    'property_type':item['property_type']})
            return _items
        else:
            return []
        
    def delete_item(self, sid):
        if sid != '':
            oid = ObjectId(sid)
            self.dao.remove({'_id':oid})
        
    def save_item(self, item, mode):
        """
        Arguments:
            user -- dictionary type
        Return:
        The '_id' value of to_save or [None] if manipulate is False and save has no _id field.
        """
        _dict = dict(item) # Clone is a must
        #if '_id' in _dict:
        #    del _dict['_id']
            
        if mode == Mode.EDIT:
            if 'id' in item.keys():
                _dict['_id'] = item['id']
        else:
            _dict['created'] = time.time()
        return self.dao.save(_dict)


class ItemValidator(Validator):
    def __init__(self):
        Validator.__init__(self)
              
        self.rules = {'title': { 
                                'required' : [None, True],
                                'minlength':[None, 1],
                                'maxlength':[None, 256]
                                },
                      'description': { 
                                'maxlength':[None, 256]
                                },
                      'price': { 
                                'numeric' : [None, True]
                                }
        }

    
class ItemForm(Form):
    ''' Submit user form
    '''
    def __init__(self):
        '''Only accept POST request
        '''
        Form.__init__(self)
        self.validator = ItemValidator()
        self.inputs = self.get_inputs()
        self.errors = self.validator.validate(self.inputs)

    def get_property_type(self, _type):
        if _type == 'room':
            return 1#PropertyType.Room
        elif _type == 'house':
            return 2#PropertyType.House
        elif _type == 'apartment':
            return 3#PropertyType.Apartment
        elif _type == 'commercial':
            return 4#PropertyType.Commercial
        else:
            return 0#PropertyType.NoneType

    def get_inputs(self):
        d = self.raw_inputs        
        address = dict([(k,v) for (k,v) in d.items() if k in ['city', 'province', 'country', 'unit', 'street', 'postcode'] ])
        address['unit'] = ''
        address['country'] = 'CA'
        address_service = AddressService()
        address_id = address_service.save_address(address, 'new')
            
        item = dict([(k,v) for (k,v) in d.items() if k not in ['city', 'province', 'country', 'unit', 'street', 'postcode'] ])
        item['_id'] = ObjectId(item['_id'])
        item['address_id'] = address_id
        item['property_type'] = self.get_property_type(item['property_type'])
        if item['price'] == '':
            item['price'] = 0
        else:
            item['price'] = int(item['price'])
        
        return item