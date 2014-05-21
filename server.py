from flask import Flask, request
from flask_login import LoginManager
from flask_principal import Principal,RoleNeed,Permission
from flask_babel import Babel, gettext as _

import os

app = Flask(__name__)


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.session_protection = "basic"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
login_manager.init_app(app)

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
