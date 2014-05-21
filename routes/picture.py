import json

from flask import jsonify
from server import app


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

@app.route('/pictures', methods=['POST'])
def save_picture(): 
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

