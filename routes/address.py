import json

from flask import jsonify
from flask_cors import cross_origin

from server import app
from services.address import AddressForm, AddressService


@app.route("/addresses", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def save_address():
    '''When a user logs in, their session is marked as 'fresh'.
    '''
    form = AddressForm()
    if form.errors == []:
        service = AddressService()
        _id = service.save_address(form.raw_inputs, form.mode)
        if _id is not None:
            return jsonify({'id':str(_id)})
        else:
            return jsonify({'id':''})
    else:
        return jsonify({'id':''})


@app.route('/users', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def get_addresses():
    users = {'hi':'hello'}
    return jsonify(user=json.dumps(users))

