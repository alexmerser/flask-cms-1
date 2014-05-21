
from flask_login import current_user
from flask import jsonify, request
from server import app
from lib.fs import FileData, FS

import json

@app.route('/pictures', methods=['POST'])
def save_picture():
    username = current_user.username
    d = json.loads(request.data)
    fdata = FileData(d['fdata'])
    fs = FS()
    fs.save('f0.'+fdata.file_ext, username, fdata.data)
    return jsonify({'success':'true'})
