from flask_login import current_user
from bson.objectid import ObjectId

class Service():
    def get_current_user(self):
        u = current_user
        return {'role': int(u.role), 'username':u.username}
    
    def get_dict(self, _dict):
        """ Convert Object in dict to string for display
        """
        ret = {}
        if isinstance(_dict, dict):
            for key in _dict:
                if isinstance(_dict[key], ObjectId):
                    ret[key] = str(_dict[key])
                else:
                    ret[key] = _dict[key]
        return ret

    def get_dao_input(self, _input, mode='new'):                
        """ Convert input to dict suitable for saving
        Arguments:
            input -- dict type
            mode -- 'edit' or 'new'
        """
        val = {}
        for key in _input:
            val[key] = _input[key]
        
        if mode == 'edit':
            val['_id'] = ObjectId(_input['_id'])
        else:
            if '_id' in _input:
                del _input['_id']
                
        return val
        
    def find(self, query={}):
        """ Return the model objects
        """
        return None