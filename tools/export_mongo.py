# These module provide data import and export
import csv
import codecs


class Exporter():
    ''' Export datas from the database to csv
    '''
    def __init__(self, db):
        """
        Arguments:
            db_name -- The database object
        """
        self.db = db
        
    def export_all(self, fname, collection, _delimiter=r';'):
        rows = []
                
        docs = self.db.find(collection)
        if docs is not None:
            heads = docs[0].keys()
            for doc in docs:
                rows.append(doc.values())

        with codecs.open(fname, "wb", "utf-8") as f:
            try:
                writer = csv.writer(f, delimiter=_delimiter, quotechar='|')
                writer.writerow(heads)
                for row in rows:
                    writer.writerow(row)
            finally:
                f.close()

        print 'export {0} done!'.format(collection)
        
            
if __name__ == '__main__':
    from db.mongodb import DBConn
    import os
    
    IMPORTED_CSV_HOME = r'imported_csv'
    EXPORTED_CSV_HOME = r'exported_csv'
    conn = DBConn()
    db = conn.get_database('shawe')
    
    exporter = Exporter(db)
    #exporter.export_all(os.path.join(IMPORTED_CSV_HOME,'cities.csv'), 'cities')
    #exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'addresses.csv'), 'addresses')
    #exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'houses.csv'), 'houses')
    #exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'users.csv'), 'users')
    #exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'categories.csv'), 'categories')
    exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'advertisements.csv'), 'advertisements')
    #exporter.export_all(os.path.join(EXPORTED_CSV_HOME,'pictures.csv'), 'pictures')
