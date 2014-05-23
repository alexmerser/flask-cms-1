# These module provide data import and export
import csv
import os
from bson.objectid import ObjectId
from bson.dbref import DBRef

class Importer():
    ''' Import datas from csv to the database
    '''
    def __init__(self, db):
        """
        Arguments:
            db_name -- The database object
        """
        self.db = db
        
    def insert(self, collection, doc):
        """ Insert a doc into collection
        Arguments:
            collection -- string type, the name of collection
            doc -- dict type
        """
        self.db.insert(collection, doc)
    
    def load(self, fname, _delimiter=r';'):
        '''Load heads and rows from the source file( default is csv file) to a buffer
        '''
        _format = os.path.splitext(fname)[1][1:].lower()
        if _format=='csv':
            # Get contents from the csv file
            with open(fname, "rb") as f:    
                try:
                    reader = csv.reader(f, delimiter=_delimiter, quotechar='|')
                    
                    _list = []
                    for row in reader:
                        _list.append(row)
                    
                    self.heads = []
                    for cell in _list[0]:
                        self.heads.append(cell.strip())
                    
                    self.rows = []
                    for row in _list[1:]:
                        item = []
                        for cell in row:
                            item.append(cell.strip())
                        self.rows.append(item)
                finally:
                    f.close()

    def find_dbref_fields(self):
        """Return the list of index if found, otherwise []
        """
        _list = []
        i = 0
        for cell in self.rows[0]:
            if 'DBRef(' in cell:
                _list.append(i)
            i += 1
        return _list
    
    def import_all(self, fname=None, collection=None, _delimiter=r';',ignore_list=[]):
        ''' Import all the columns from csv file to the database.collection
        Arguments:
            collection -- string type, the name of the collection
        '''
        self.load(fname, _delimiter)
        
        index_list = self.find_dbref_fields()
        
        if '_id' in self.heads:
            id_col = self.heads.index('_id')
        
            for row in self.rows:
                _dict = {}
                i = 0
                for cell in row:
                    if self.heads[i] not in ignore_list:
                        if i == id_col:
                            _dict[self.heads[i]] = ObjectId(cell)
                        elif i in index_list: # If it's an DBRef type
                            _dict[self.heads[i]] = eval(cell).id
                        else:
                            _dict[self.heads[i]] = cell
                    i += 1
                print _dict
                self.db.save(collection, _dict)                    
        else:
            for row in self.rows:
                _dict = {}
                i = 0
                for cell in row:
                    if self.heads[i] not in ignore_list:
                        _dict[self.heads[i]] = cell
                    i += 1
                print _dict
                self.db.save(collection, _dict)
            
        print 'import data from {0} to collection {1} --- Done!'.format(fname, collection)


    def remove_all_collections(self):
        for collection in ['cities','addresses','users','houses','advertisements','pictures']:
            self.db.remove(collection)
        #print 'import data from {0} to collection {1} --- Done!'.format(fname, collection)        
    
            
    # Private call only
    def _abbrev_province(self, fname):
        '''Convert province column to abbrevation
        '''
        provinces = {'Alberta':'AB',
                    'British Columbia':'BC',
                    'Manitoba':'MB',
                    'New Brunswick':'NB',
                    'Newfoundland':'NL',
                    'Northwest Territories':'NT',
                    'Nova Scotia':'NS',
                    'Nunavut':'NU',
                    'Ontario':'ON',
                    'Prince Edward Island':'PE',
                    'Quebec':'QC',
                    'Saskatchewan':'SK',
                    'Yukon':'YT'}
        
        with open(fname, 'wb') as f:    
            try:
                parser = csv.writer(f, delimiter=';', quotechar='|')
                parser.writerow(self.head)
                keys = provinces.keys()
                for cells in self.rows:
                    cells[0] = cells[0].strip()
                    cells[1] = cells[1].strip()
                    if cells[1] in keys:
                        cells[1] = provinces[cells[1]]
                        parser.writerow(cells)
            finally:
                f.close()
            
if __name__ == '__main__':
    from lib.mongodb import DBConn
    from config import cfg
    import os
    
    IMPORTED_CSV_HOME = r'imported_csv'
    EXPORTED_CSV_HOME = r'exported_csv'
    conn = DBConn()
    db = conn.get_database(cfg.database)
    
    #exporter = Exporter(db)
    #exporter.export_all(os.path.join(IMPORTED_CSV_HOME,'cities.csv'), 'cities')
    #exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'addresses.csv'), 'addresses')
    #exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'houses.csv'), 'houses')
    
    importer = Importer(db)
    importer.import_all(os.path.join(EXPORTED_CSV_HOME,'addresses.csv'),'addresses')
    """
    importer.remove_all_collections()
    
    importer.import_all(os.path.join(EXPORTED_CSV_HOME,'cities.csv'),'cities')
    importer.import_all(os.path.join(EXPORTED_CSV_HOME,'addresses.csv'),'addresses')
    importer.import_all(os.path.join(EXPORTED_CSV_HOME,'users.csv'), 'users')
    importer.import_all(os.path.join(EXPORTED_CSV_HOME,'houses.csv'), 'houses')
    """
    
    #importer.import_all(os.path.join(EXPORTED_CSV_HOME,'advertisements.csv'), 'advertisements')
    #importer.import_all(os.path.join(EXPORTED_CSV_HOME,'pictures.csv'), 'pictures')
    #importer.import_all(os.path.join(EXPORTED_CSV_HOME,'categories.csv'),'categories')
