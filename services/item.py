from model.item import ItemDao
from lib.validator import Validator
from lib.form import Form
from bson.objectid import ObjectId
from bson.dbref import DBRef

from services import Service

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
        if '_id' in _dict:
            del _dict['_id']
            
        if mode == Mode.EDIT:
            if 'id' in user.keys():
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
        self.errors = self.validator.validate(self.raw_inputs)
