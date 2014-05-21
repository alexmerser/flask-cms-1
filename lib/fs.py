import shutil    
import os
import base64

class FileData():
    def __init__(self, fdata):
        """
        Arguments:
            fdata -- come from html5 js code, FileReader.result
        """
        info, data = fdata.split(',')
        _type, self.encoding = info.split(';')
        self.file_type, self.file_ext = _type.split(r'/')

        self.data = base64.b64decode(data)


class FS:
    def _save(self, fpath, data):
        """ Save data to file, if file exist, overwrite it.
        Arguments:
            data -- The content of the file
            fpath -- The file path  
        """
        f = open(fpath, 'wb' )
        f.write(data)
        f.close()
            
    def save(self, fname, path, data):
        """ Save file to the path, if file exist, overwrite it.
            if path does not exist, create it and it's all intermediate-level directories needed 
        Arguments:
            fname -- The name of the file
            path -- The path of the dir where the file locates   
        """
        fpath = os.path.join( path, fname )
        
        if os.path.exists(fpath) and os.path.isfile(fpath):
            os.remove(fpath)
            self._save(fpath, data)
        else:
            if os.path.exists(path):
                self._save(fpath, data)
            else:
                os.makedirs(path)
                self._save(fpath, data)

    def get_all(self, path):
        """ Get all the items name under a folder
        Arguments:
            path -- The path of the dir where the files locate  
        """
        return os.listdir(path)
    
    def remove(self, fname, path):
        """
        Arguments:
            fname -- The name of the file
            path -- The path of the dir where the file locates   
        """
        fpath = os.path.join( path, fname )
        if os.path.exists(fpath) and os.path.isfile(fpath):
            os.remove(fpath)

    def remove_tree( self, path ):
        """
        Arguments:
            path -- The path of the dir where the files locate  
        """
        if os.path.isdir(path):
            shutil.rmtree(path)

if __name__ == "__main__":
    # Testing
    fs = FS()
    path = r'c:\workspace\opt\testing'
    fname = 'hi.txt'
    
    fs.save(fname, path,'123456')
    if os.path.isfile(os.path.join(path, fname)):
        print 'create file success\n'

    items = fs.get_all(path)
    print items

    fs.remove(fname, path)
    if not os.path.isfile(os.path.join(path, fname)):
        print 'remove file success\n'
        
    fs.remove_tree(path)
    if not os.path.exists(path):
        print 'remove tree success\n'
