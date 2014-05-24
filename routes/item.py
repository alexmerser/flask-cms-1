
from flask_login import current_user
from flask import jsonify, request
from flask_cors import cross_origin

from server import app
from lib.fs import FileData, FS
from services.item import ItemForm, ItemService
 
import json


@app.route('/items', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def save_item():
    item_form = ItemForm()
    item_service = ItemService()
    item_service.save_item(item_form.inputs, item_form.mode)
    
    return jsonify({'success':'true'})



@app.route('/pictures', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def save_picture():
    username = current_user.username
    d = json.loads(request.data)
    fdata = FileData(d['fdata'])
    fs = FS()
    fs.save('f0.'+fdata.file_ext, username, fdata.data)
    return jsonify({'success':'true'})
