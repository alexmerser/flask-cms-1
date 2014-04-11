from flask import Flask, request
from flaskext.uploads import UploadSet, IMAGES
import os
from flask_principal import Principal,RoleNeed,Permission
from flask_babel import Babel, gettext as _
'''
The Flask application object creation has to be in the __init__.py file. 
That way each module can import it safely and the __name__ variable will resolve to the correct package.
'''
app = Flask(__name__)

'''
app.config['UPLOADS_FOLDER'] = os.path.realpath('.')
app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
app.config['UPLOADED_FILES_ALLOW']=IMAGES
'''

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.session_protection = "basic"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
login_manager.init_app(app)

#from jinja2 import Environment
#def _(_text):
#    return _text

#app.jinja_env.globals.update(_=_)
#env = Environment()
#env.globals['_'] = _


# flask-principal
'''
principals = Principal()
user_role = RoleNeed('user')
user_permission = Permission(user_role)

admin_role = RoleNeed('admin')
admin_permission = Permission(admin_role)


principals._init_app(myapp)

#myapp.config.from_pyfile('babel.cfg')
babel = Babel(myapp)
myapp.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
'''