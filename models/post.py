from model import Model, Dao


class Post(Model):
    def __init__(self, _dict):
        """Arguments:
            _dict
        """
        Model.__init__(self, _dict)
        
        self.body = _dict['body']
        self.created = _dict['created']
        
        # Associated field
        self.author = _dict['author']
        self.subject = _dict['subject']
        

    def __repr__(self):
        return '<Post %r>' % (self.body)


class PostDao(Dao):
    def __init__(self):
        Dao.__init__(self, Post)
        self.collection = 'posts'

        # associates { field name : collection name }
        self.ref_collections = {'author':'users', 'subject':'subjects'}
        
if __name__ == '__main__':
    # create table
    pass