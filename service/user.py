from model.user import User, UserDao
from lib.validator import Validator
from lib.form import Form

from flask import request
from flask_login import login_user
import time
from bson.objectid import ObjectId

class UserService():
    def __init__(self):
        """Arguments:
            name -- string type
            item_id -- BSON ObjectId type
        """
        self.dao = UserDao()
        self.roles = ['Admin', 'User']
        self.titles = ['Project Manager', 'Team Lead', 'Developer', 'Tester'] # The order should confirm with users.html
        
    def get_role(self, role):
        if role < len(self.roles):
            return self.roles[role]
        else:
            return 'None'
    
    def get_title(self, title):
        if title < len(self.titles):
            return self.titles[title]
        else:
            return 'None'
        
    def get_user(self, sid):
        """
        Argument:
            sid -- string type
        """
        if sid != '':
            oid = ObjectId(sid)
            user = self.dao.find_one({'_id':oid})
            return {'id':str(user['_id']),
                    'username':user['username'],
                    'email':user['email'],
                    'phone':user['phone'],
                    'created':user['created'],
                    'role':self.get_role(user['role']),
                    'title':self.get_title(user['title'])}
        else:
            return None
        
    def delete_user(self, sid):
        if sid != '':
            oid = ObjectId(sid)
            self.dao.remove({'_id':oid})
            
    def get_users(self, query={}):
        """ Get the users for rendering the html
        """
        users = self.dao.find(query)
        
        if users is not None:
            _users = []
            for user in users:
                _users.append({'id':str(user['_id']),
                                'username':user['username'],
                                'email':user['email'],
                                'role':self.get_role(user['role']),
                                'title':self.get_title(user['title'])})
            return _users
        else:
            return []
        

    def submit_user(self, inputs):
        """
        Return:
        The '_id' value of to_save or [None] if manipulate is False and to_save has no _id field.
        """
        _dict = {'username':inputs['username'],
                 'password':inputs['password'],
                'email':inputs['email'],
                'phone':inputs['phone'],
                'role':inputs['role'],
                'title':inputs['title'],
                }

        if inputs['mode'] == 'edit':
            _dict['created'] = inputs['created']
            if 'id' in inputs.keys():
                _dict['_id'] = inputs['id']
        else:
            _dict['created'] = time.time()
        return self.dao.save(_dict)


    
    def login(self, account, password, remember_me=False):
        """
        Arguments:
            account: string type, can be username or email address
            password: string type
        Return 
            True if the log in attempt succeeds, otherwise False
        """
        user = self.dao.find_one({'email':account, 'password':password})
        if user is None:
            user_dict = self.dao.find_one({'username':account, 'password':password})
            if user_dict is None:
                return False
            else:
                return login_user(User(user_dict), remember=remember_me)
        else:
            return login_user(User(user_dict), remember=remember_me)
            
    def signup(self, form):
        """
        Return:
            The '_id' value of to_save or [None] if manipulate is False and to_save has no _id field.
        """
        if form.errors == []:
            return self.dao.save({'username':form.username,
                         'password':form.password,
                         'email':form.email,
                         'role':0, # Normal user
                         'title':0,
                         'phone':form.phone,
                         'description':form.description,
                         'created':time.time()}) 
        return None




class UserValidator(Validator):
    def __init__(self):
        Validator.__init__(self)
              
        self.rules = {'username': { 
                                'required' : [None, True],
                                'maxlength':[None, 32]},
                      'password':{'required' : [None, True],
                                  'minlength':[None, 8],
                                  'maxlength':[None, 32]
                               },
                      'email': { 
                                'required' : [None, True],
                                'maxlength':[None, 64],
                                'unique' : [self.unique, 'email', 'This email exists, please try another.']
                                }
        }

    def unique(self, val, field_name):
        _dao = UserDao()
        ret = _dao.find_one({field_name:val})
        return ret is None
    
    
class UserForm(Form):
    """ Submit user form
    """
    def __init__(self):
        """Only accept POST request
        """
        Form.__init__(self)
        self.validator = UserValidator()
        
        if self.is_submitted():
            self.raw_inputs = self.get_raw_input()
            self.inputs = self.get_inputs(self.raw_inputs)
            self.errors = self.validator.validate(self.inputs)
            if self.errors == []:
                self.username = self.request.values.get('username')
                self.password = self.request.values.get('password')
                self.email = self.request.values.get('email')
                self.role = self.request.values.get('role')
                self.title = self.request.values.get('title')
                self.phone = self.request.values.get('phone')
                
    def get_inputs(self, raw_inputs):                
        """ Convert inputs type
        """
        return {'mode': raw_inputs['mode'],
                'id':raw_inputs['id'],
                'username': raw_inputs['username'],
                'password': raw_inputs['password'],
                'email': raw_inputs['email'],
                'role': int(raw_inputs['role']),
                'title': int(raw_inputs['title']),
                'phone': raw_inputs['phone']
        }
    

class LoginValidator(Validator):
    def __init__(self, account):
        self.account = account
        
        Validator.__init__(self)
        
        self.dao = UserDao()
        self.rules = {'account': { 
                                'account_valid' : [self.account_valid, 'email', 'The account does not exist.']
                                },
                      'password':{
                                'password_valid' : [self.password_valid, 'password', 'Wrong password']
                               }
                    }

    def account_valid(self, val, field_name):
        _dao = UserDao()
        user = _dao.find_one({'email':val})
        if user is None:
            user = _dao.find_one({'username':val})
            return user is not None
        else:
            return True

    def password_valid(self, val, field_name):
        account = self.account
        
        user = self.dao.find_one({'email':account})
        if user is None:
            user = self.dao.find_one({'username':account})
            if user is None:
                return False
            else:
                return user['password'] == val
        else:
            return user['password'] == val
       
class LoginForm(Form):
    def __init__(self):
        '''Only accept POST request
        Note: account can be username or email address
        '''
        Form.__init__(self)
        account = self.request.values.get('account')
        
        self.validator = LoginValidator(account)
        
        if self.is_submitted():
            self.errors = self.validator.validate(self.input)
            if self.errors == []:
                # If get fail, return None
                self.account = self.request.values.get('account')
                self.password = self.request.values.get('password')
                if self.request.form.getlist('remember-me') == []:
                    self.remember_me = False
                else:
                    self.remember_me = True
                
    

