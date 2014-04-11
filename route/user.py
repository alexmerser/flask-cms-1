from flask import render_template,redirect,url_for,session,request,jsonify
from flask_login import login_user, login_required, logout_user, current_user

from bson.objectid import ObjectId

from service.user import UserService, UserForm
from controller import app
from core import login_manager
from model.user import User, UserDao
import json


@login_manager.user_loader
def load_user(_id):
    """This is a callback for the LoginManager class, it is used to reload the user object from the user ID stored in the session. 
    Arguments 
        _id -- The unicode string type, ID of a user
    Return 
        -- The user object if ID is valid, otherwise return None
    """
    user_dao = UserDao()
    user_dict = user_dao.find_one({'_id':ObjectId(_id)})
    
    return User(user_dict)


@app.route('/validate_signup')
@app.route('/validate_signup', methods=['GET','POST'])
def validate_signup():
    """ Ajax validation for multiple submit pages
    """
    form = UserForm()
    return jsonify(errors=form.errors)


@app.route("/signup", methods=["GET","POST"])
def signup():
    form = UserForm()
    service = UserService()
    if form.is_submitted():
        if service.signup(form):
            return render_template('login.html')
        else:
            return render_template('signup.html', errors_json=json.dumps(form.errors))
    else:
        return render_template('signup.html', errors_json=[])
    

    

@app.route('/manage_users')
@app.route('/manage_users', methods=['GET','POST'])
def manage_users():
    '''When a user logs in, their session is marked as 'fresh'.
    '''
    user_service = UserService()
    _users = user_service.get_users()
    return render_template('users.html', users=json.dumps(_users), errors_json=[])


@app.route('/display_users')
@login_required
def display_users():
    _serv = UserService()
    _users = _serv.get_users()
    if session['errors_json'] == '':
        return render_template('users.html', users=json.dumps(_users), errors_json=[])
    else:
        errors = session['errors_json']
        return jsonify(items=json.dumps(errors))



@app.route('/submit_user', methods=['GET','POST'])
#@login_required
def submit_user():
    form = UserForm()
    if form.is_submitted():
        if form.has_error():
            session['errors_json'] = json.dumps(form.errors)
            return redirect(url_for('display_users'))#errors_json=json.dumps(form.errors)))
        else:
            session['errors_json'] = []
            service = UserService()
            user_id = service.submit_user(form.inputs)
            return redirect(url_for('manage_users')) 

""" The following are Restful APIs
"""
@app.route('/users', methods=['GET'])
@login_required
def get_users():
    serv = UserService()
    users = serv.get_users()
    return jsonify(user=json.dumps(users))


@app.route('/users/<string:sid>', methods=['GET'])
@login_required
def get_user():
    sid = request.values['sid']
    serv = UserService()
    user = serv.get_user(sid)
    return jsonify(user=json.dumps(user))

@app.route('/delete_users')
@app.route('/delete_users', methods=['GET','POST'])
def delete_users():
    """ This is an Ajax handler
    """
    sid = request.values['sid']
    serv = UserService()
    serv.delete_user(sid)
    _users = serv.get_users()
    
    return jsonify(projects=json.dumps(_users))  