
from flask_login import current_user
from flask import jsonify, request
from flask_cors import cross_origin

from server import app
from lib.fs import FileData, FS
from services import Service
from services.item import ItemForm, ItemService, ItemPictureService

from bson.objectid import ObjectId
import os 
import json

SERVER_PATH = r'..\angular-cms\app'

@app.route('/items', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def save_item():
    item_form = ItemForm()
    item_service = ItemService()
    item_service.save_item(item_form.inputs, item_form.mode)
    
    return jsonify({'success':'true'})

@app.route('/items', methods=["GET"])
@cross_origin(headers=['Content-Type'])
def get_items():
    item_service = ItemService()
    pic_service = ItemPictureService()
    items = item_service.get_items()
    _items = []
    for item in items:
        pics = pic_service.get_item_pictures({'item_id':ObjectId(item['id']), 'order':1})
        if pics != []:
            item['picture_path'] = pics[0]['fpath']
        else:
            item['picture_path'] = ''
        _items.append(item)
    return jsonify(items=json.dumps(_items))

@app.route('/object_id', methods=["GET"])
@cross_origin(headers=['Content-Type'])
def get_object_id():
    s = Service()
    _id = s.get_object_id()    
    return jsonify(id=_id)

@app.route('/pictures', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def save_pictures():
    _service = ItemPictureService()
    d = json.loads(request.data)
    username = d['username']
    pictures = d['pictures']
    _pics = {}
    
    for name in pictures:
        if pictures[name] != '':
            fdata = FileData(pictures[name])            
            fs = FS()
            path = os.path.join(r'images', username, d['id'])
            fname = name + '.'+fdata.file_ext
            # Save picture
            fs.save(fname, os.path.join(SERVER_PATH, path), fdata.data)
            
            # Save information to database
            order = int(name.lstrip('f'))
            fpath = os.path.join(path, fname)
            _id = _service.save_item_picture({'fpath':fpath, 'item_id':ObjectId(d['id']), 'order':order}, 'new')
            _pics[name]=_id
        else:
            _pics[name]=''
            
    return jsonify(pictures=json.dumps(_pics))


@app.route('/itemPictures', methods=["GET"])
@cross_origin(headers=['Content-Type'])
def get_item_pictures():
    _service = ItemPictureService()
    items = _service.get_item_pictures()    
    return jsonify(items=json.dumps(items))

