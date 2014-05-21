from mongodb import DBConn
from datetime import datetime
from bson.dbref import DBRef
from bson.objectid import ObjectId
from app.config import cfg

db_conn = DBConn()
db = db_conn.get_database(cfg.database)

class Model():
    def __init__(self, _dict): 
        # The id field hold ObjectId
        if '_id' in _dict.keys():
            self._id = _dict['_id']
        

class Dao():
    """ Data Access class
    """
    def __init__(self, ModelClass):
        self.db = db
        self.ModelClass = ModelClass

    def get_time_string(self, timestamp):
        s = datetime.fromtimestamp(timestamp)
        return s.strftime('%Y-%m-%d %H:%M:%S')

    def save(self, model):
        """Updates an existing document, if _id field exists, otherwise inserts a new document.
        Arguments:
            model --- Can be Model type or dict type, the associated field must be ObjectId
        Return:
            The '_id' value of to_save or [None] if manipulate is False and to_save has no _id field.
        """
        # The ID field must exist
        if isinstance(model, dict):
            return self.db.save(self.collection, model)
        else:
            _dict = model.__dict__
            return self.db.save(self.collection, _dict)

    def update(self, query, values):
        """Updates an existing document, if _id field exists, otherwise inserts a new document.
         * Update support $set,$unset
        Arguments:
            model --- Can be Model type or dict type, the associated field must be ObjectId
        Return:
            The '_id' value of to_save or [None] if manipulate is False and to_save has no _id field.
        """
        # The ID field must exist
        if isinstance(values, dict):
            #def update(self, query, values, collection_name, multi_update=False)
            return self.db.update(query, values, self.collection)
        else:
            _dict = values.__dict__
            return self.db.update(query, _dict, self.collection)
         
    def remove(self, model):
        """
        Arguments:
            model -- dict type or Model object type
        Return:
            A document (dict) describing the effect of the remove or None if write acknowledgement is disabled.
        """
        if isinstance(model, dict):
            return self.db.remove(self.collection, query={'_id':model['_id']})
        else:
            if model._id is not None:
                return self.db.remove(self.collection, query={'_id':model._id})
            else:
                return None
    
    def find_one(self, query={}):
        """
        Arguments:
            query --- The dict type
        Return:
            Raises TypeError if any of the arguments are of improper type. 
            Returns an instance of Cursor corresponding to this query.
        """
        return self.db.find_one(self.collection, query)

    
    def find(self, query={}):
        """
        Arguments:
            query --- The dict type
        Return:
            Raises TypeError if any of the arguments are of improper type. 
            Return array of the ModelClass.
        """
        cursor = self.db.find(self.collection, query=query)
        
        models = []
        for _dict in cursor:
            if _dict is not None:
                models.append( _dict )
        
        return models
    
    def all(self, order=None):
        return self.find()
    
