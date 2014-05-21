import json
from flask_login import current_user
from flask import jsonify
from app import app
from flask import request
from app.lib.fs import FileData, FS

@app.route('/pictures', methods=['POST'])
def save_picture():
    username = current_user.username
    d = json.loads(request.data)
    fdata = FileData(d['fdata'])
    fs = FS()
    fs.save('f0.'+fdata.file_ext, username, fdata.data)
    return jsonify({'success':'true'})