from flask import request, session, current_app

class Mode:
    NEW, EDIT = range(2)
    
class Form():
    
    def __init__(self):
        self.request = request
        if request is not None:
            self.raw_inputs = self.get_raw_inputs(request)

            if '_mode' in self.raw_inputs:
                self.mode = self.raw_inputs['_mode']
                del self.raw_inputs['_mode']
                
                if self.mode == Mode.NEW and '_id' in self.raw_inputs:
                    del self.raw_inputs['_id']
            else:
                self.mode = Mode.NEW # NEW by default
                
    def is_submitted(self):
        """
        Checks if form has been submitted. The default case is if the HTTP
        method is **PUT** or **POST**. 
        
        The POST request method is designed to accept data in the request message, often used when 
        uploading or submitting a web form.
        
        The GET request method is designed to retrieve information from the server
        """
        return request and request.method in ("PUT", "POST")
 
    def get_raw_inputs(self, req):
        """Get raw inputs from the form, group into a map and return this map.
        """
        """
        values = {}
        for key in vals:
            values[key] = vals[key]
        return values
        """
        if 'application/json;' in req.content_type.lower():
            return dict(req.json)
        else:
            return dict(req.values.items())
    
    def has_error(self):
        return self.errors != []