from model import Model, Dao

class User(Model):
    def __init__(self, _dict):
        Model.__init__(self, _dict)
         
        self.username = _dict['username']
        self.password = _dict['password']
        self.email = _dict['email']
        self.phone = _dict['phone']
        self.role = _dict['role'] # Admin and None Admin
        self.title = _dict['title'] # PM, developer, tester
        self.created = _dict['created']
        #datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<User %r>' % (self.username)
    
    #Flask-Login required functions
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """Get Object ID string
        """
        if self._id is not None:
            return unicode(self._id)
        else:
            return u''



class UserDao(Dao):
    def __init__(self):
        """Arguments:
            collection --- string the name of the collection
        """
        Dao.__init__(self, User)
        self.collection = 'users'


        
if __name__ == '__main__':
    pass
