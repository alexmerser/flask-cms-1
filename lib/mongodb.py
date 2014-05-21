"""
This is a wrapper layer of pymongo
"""
import pymongo
from pymongo.errors import ConnectionFailure

import sys

class DBConn:
    """Database Connection, Low level MongoDB access API. The method parameters are dictionaries.
    The implementation uses mongo_client for a pooled mongodb.
    
    """
    def __init__(self, host="localhost", port=27017):
        """Create new connection to a single MongoDB instance
        """
        try:
            #The self.conn object has connection-pooling built in.
            #It also performs auto-reconnection when necessary.
            self.conn = pymongo.MongoClient(host, auto_start_request=False)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)

    def get_database(self, db_name):
        return Database(self.conn, db_name)


class Database:
    def __init__(self, db_conn, db_name, page_size=1):
        self.page_size = int(page_size)
        self.db = db_conn[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert(self, collection_name, doc):
        '''insert a document into a collection, result could be 
        a list of objects id, an id object or None
        Return:
            object id
        '''
        return self.db[collection_name].insert(doc, safe=True)
    
    def save(self, collection_name, _dict):
        """Updates an existing document or inserts a new document, depending on its document parameter.
        Arguments:
            model --- The Model object with id
        Return:
            The '_id' value of to_save or [None] if manipulate is False and to_save has no _id field.
        """
        # The ID field must exist
        return self.db[collection_name].save(_dict)
        
    def update(self, query, values, collection_name, multi_update=False):
        '''
        Return:
            object id
        '''
        return self.db[collection_name].update(query, values,\
                safe=True, multi=multi_update)
    
    def remove(self, collection_name, query={}):
        '''remove the documents by query, return null if no document affected
        Return:
            A document (dict) describing the effect of the remove or None if write acknowledgement is disabled.
        '''
        return self.db[collection_name].remove(query)
    
    def find_one(self, collection_name, query = {}):
        """Return:
            single document
        """
        return self.db[collection_name].find_one(query)
    
    def find(self, collection_name, page_num = 1, 
             sort_field = None, 
             sort_direction = pymongo.DESCENDING,
             query = {}):
        """ only return the records with the page size
        Return
            Cursor object
        """
        result = self.db[collection_name].find(query)#\
                #.sort([(sort_field,sort_direction)]).limit(self._page_size)
        return result