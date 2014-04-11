from flask import request, session, current_app
    
class Form():
    
    def __init__(self):
        self.request = request
        if self.is_submitted():
            self.input = self.get_raw_input()
            
            # Clean up the hidden input
            if '_mode' in self.input:
                self.mode = self.input['_mode']
                del self.input['_mode']
                
                if self.mode == 'new' and '_id' in self.input:
                    del self.input['_id']
                
    def is_submitted(self):
        """
        Checks if form has been submitted. The default case is if the HTTP
        method is **PUT** or **POST**. 
        
        The POST request method is designed to accept data in the request message, often used when 
        uploading or submitting a web form.
        
        The GET request method is designed to retrieve information from the server
        """
        return request and request.method in ("PUT", "POST")
 
    def get_raw_input(self):
        """Get raw inputs from the form, group into a map and return this map.
        """
        values = {}
        for key in request.values:
            values[key] = request.values[key]
        return values

    def has_error(self):
        return self.errors != []