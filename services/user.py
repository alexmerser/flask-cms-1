from app.models.user import Role, User, UserDao
from app.lib.validator import Validator
from app.lib.form import Form, Mode

from flask import request
from flask_login import login_user
import time
from bson.objectid import ObjectId


    
class LoginError():
    NO_ERROR, USER_NOT_EXIT, WRONG_PASSWORD = range(3)

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
        

    def save_user(self, user, mode):
        """
        Arguments:
            user -- dictionary type
        Return:
        The '_id' value of to_save or [None] if manipulate is False and to_save has no _id field.
        """
        _dict = dict(user) # Clone user is a must
        if '_id' in _dict:
            del _dict['_id']
            
        if mode == Mode.EDIT:
            if 'id' in user.keys():
                _dict['_id'] = user['id']
        else:
            _dict['created'] = time.time()
        return self.dao.save(_dict)


    
    def login(self, account, password, remember_me=False):
        """
        Arguments:
            account: string type, can be username or email address
            password: string type
        Return 
            True if the log in attempt succeeds, otherwise Error code
        """
        user = self.dao.find_one({'$or':[{'email':account}, {'username':account}]})
        if user is None:
            return LoginError.USER_NOT_EXIT
        else:
            if user['password'] == password:
                login_user(User(user), remember=remember_me)
                return LoginError.NO_ERROR
            else:
                return LoginError.WRONG_PASSWORD
            

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
        self.errors = self.validator.validate(self.raw_inputs)
            

    

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
        user = _dao.find_one({'$or':[{'email':val},{'username':val}]})
        if user is None:
            return False
        else:
            return True

    def password_valid(self, val, field_name):
        account = self.account        
        user = self.dao.find_one({'$or':[{'email':account},{'username':account}]})
        if user is None:
            return False
        else:
            return user['password'] == val
        
class LoginForm(Form):
    def __init__(self):
        '''Only accept POST request
        Note: account can be username or email address
        '''
        Form.__init__(self)
        account = self.raw_inputs['account']
        
        self.validator = LoginValidator(account)
        
        if self.is_submitted():
            self.errors = self.validator.validate(self.raw_inputs)
            #if self.errors == []:
                # If get fail, return None
            self.account = self.raw_inputs['account']
            self.password = self.raw_inputs['password']
            self.remember_me = self.raw_inputs['remember']
                
    

