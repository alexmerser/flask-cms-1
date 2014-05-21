
from lib.validator import Validator
from lib.form import Form
from model.post import PostDao
from model.user import UserDao
from services import Service

from bson.dbref import DBRef
from flask import request
from flask_login import login_user, current_user

import time



class PostService(Service):
    def __init__(self):
        self.dao = PostDao()
        self.user_dao = UserDao()
        self.subject_dao = SubjectDao()
    
    def get_post_list(self):
        posts = []
        _posts = self.dao.all()
        for _post in _posts:
            author = self.user_dao.find_one({'_id':_post.author.id})
            subject = self.subject_dao.find_one({'_id':_post.subject.id})
            if _post.subject is not None:
                posts.append({"body":_post.body, 
                              "subject":subject.body, 
                              "author":author.username,
                              "created":_post.created})
            else:
                posts.append({"body":_post.body,
                              "subject":None,
                              "author":author.username,
                              "created":_post.created})
        return posts


    def submit_post(self, form):
        if form.mode == 'edit':
            #post = post_dao.update_post(form.id, form.name, form.description)
            pass
        elif form.mode == 'new':
            subject = self.subject_dao.find_one({'body':form.subject})
            if subject is None:
                subject_id = self.subject_dao.save({'body':form.subject})
            
            _dict = {'body':form.body,
                     'created': time.time(),
                     'author': DBRef('users', form.author._id)}
            
            if subject is None:
                _dict['subject'] = DBRef('subjects', subject_id)
            else:
                _dict['subject'] = DBRef('subjects', subject._id)
                
            self.dao.save(_dict)


class PostValidator(Validator):
    def __init__(self):
        Validator.__init__(self)
              
        self.rules = {'body': { 
                                'required' : [None, True],
                                'minlength':[None, 1],
                                'maxlength':[None, 256]
                                }
        }

    
class PostForm(Form):
    """ Submit user form
    """
    def __init__(self):
        """Only accept POST request
        """
        Form.__init__(self)
        self.validator = PostValidator()
        
        if self.is_submitted():
            inputs = self.get_raw_inputs()
            self.errors = self.validator.validate(inputs)
            if self.errors == []:
                self.subject = self.request.values.get('subject')
                self.body = self.request.values.get('body')
                self.mode = self.request.values.get('mode')
                self.author = current_user
                
                
    def has_error(self):
        return self.errors != []
