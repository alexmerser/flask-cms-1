import json

from flask import jsonify, request
from flask_cors import cross_origin

from server import app
from services.address import AddressForm, AddressService, CityService

# /cities?province=ON,AB;country=CA
@app.route('/cities/<query>', methods=["GET"])
@cross_origin(headers=['Content-Type'])
def get_cities(query):
    query_string = request.query_string
    
    if ';' in query_string:
        query = {}
        args = query_string.split(';')
        for arg in args:
            k,v = arg.split('=')
            query[k] = v
    else:
        k,v = query_string.split('=')
        query[k] = v
        
    c = CityService()
    cities = c.get_cities(query)    
    return jsonify(cities=json.dumps(cities))

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

