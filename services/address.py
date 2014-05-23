from models.address import AddressDao
from models.city import CityDao
from services import Service
from lib.validator import Validator
from lib.form import Form

from bson.dbref import DBRef


class AddressService(Service):
    def __init__(self):
        self.dao = AddressDao()
        self.city_dao = CityDao()
        
    def get_addresses(self, query={}):
        """ Get address for display
        """
        addresses = []
        _addresses = self.dao.all()
        for _address in _addresses:
            c = self.city_dao.find_one({'_id':_address['city_id']})
            addresses.append({"street":_address['street'],
                              "city":"{0} {1} {2}".format(c['city'], c['province'], c['country']),
                              "postcode":_address['postcode']})
        return addresses


    def save_address(self, inputs, mode):
        if mode == 'edit':
            #address = address_dao.update_address(inputs['id, inputs['name, inputs['description)
            return None
        elif mode == 'new':
            city_dict = {'city':inputs['city'], 'province':inputs['province'], 'country':inputs['country']}
            city = self.city_dao.find_one(city_dict)
            
            _dict = {'unit':inputs['unit'], 
                     'street':inputs['street'], 
                     'postcode':inputs['postcode']}
            
            if city is None:
                city_id = self.city_dao.save(city_dict)
                _dict['city_id'] = city_id
            else:
                _dict['city_id'] = city._id
                
            return self.dao.save(_dict)


class AddressValidator(Validator):
    def __init__(self):
        Validator.__init__(self)
              
        self.rules = {'street': { 
                                'required' : [None, True],
                                'minlength':[None, 1],
                                'maxlength':[None, 256]
                                }
        }

    
class AddressForm(Form):
    """ Submit user form
    """
    def __init__(self):
        """Only accept POST request
        """
        Form.__init__(self)
        self.validator = AddressValidator()
        
        if self.is_submitted():
            self.raw_inputs = self.get_raw_inputs()
            self.errors = self.validator.validate(self.raw_inputs)
