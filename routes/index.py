import json

from flask import jsonify
from flask_cors import cross_origin
from flask_login import current_user

from server import app
from services.user import LoginForm, UserForm, UserService

@app.route('/')
def root():
    return app.send_static_file('index.html')
    #return make_response(open('index.html').read())

@app.route("/login", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def login():
    '''When a user logs in, their session is marked as 'fresh'.
    '''
    form = LoginForm()
    if form.errors == []:
        service = UserService()
        ret = service.login(form.account, form.password, form.remember_me)
        return jsonify({'error':str(ret),'username':current_user.username})
    else:  # If input has error
        return jsonify({'error':str(form.errors[0])})

"""
@app.route("/users", methods=["GET","POST"])
def signup():
    form = UserForm()
    service = UserService()
    if form.is_submitted():
        _id = service.save_user(form.raw_inputs)
        if _id is not None:
            return jsonify(user=json.dumps({'id':_id}))
        else:
            return jsonify(user=json.dumps({'id':_id}))
    else:
        return render_template('signup.html', errors_json=[])
"""    
# Restful API

@app.route('/users', methods=['POST'])
def save_user(): 
    form = UserForm()
    service = UserService()
    if form.is_submitted():
        _id = service.save_user(form.raw_inputs, form.mode)
        if _id is not None:
            return jsonify({'id':str(_id)})
        else:
            return jsonify({'id':''})
    else:
        return jsonify({'id':''})


@app.route('/users', methods=['GET'])
def get_users():
    users = {'hi':'hello'}
    return jsonify(user=json.dumps(users))

