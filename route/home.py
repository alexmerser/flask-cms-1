from flask import render_template, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user

from bson.objectid import ObjectId

#from service.project import ProjectService
#from service.sprint import SprintService

#from service.user import UserService, LoginForm, UserForm


from route import app

import json

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    '''When a user logs in, their session is marked as 'fresh'.
    '''
    if '_fresh' in session.keys() and session['_fresh']:
        return render_template('items.html')
        '''
        sprint_service = SprintService()
        _sprints = sprint_service.get_sprints({'project_id':ObjectId(_projects[0]['id'])})
        if _sprints == []:
            return render_template('index.html', projects=json.dumps(_projects), sprints=[],  username=current_user.username)
        else:
            return render_template('index.html', projects=json.dumps(_projects), sprints=json.dumps(_sprints), username=current_user.username)
        '''
    else:
        #return render_template('index.html', projects=[], sprints=[], username=None)
        return redirect(url_for("login"))
"""    
@app.route("/login", methods=["GET", "POST"])
def login():
    '''When a user logs in, their session is marked as 'fresh'.
    '''
    form = LoginForm()
    if form.is_submitted():
        if form.errors == []:
            service = UserService()
            ret = service.login(form.account, form.password)
            # flash('Logged in successfully!')
            # return render_template('products.html', mytest = 'You logged in')
            # return render_template('setting.html')
            if ret:
                return redirect(url_for("index"))
            # return redirect(request.args.get("next") or url_for("index"))
            else:
                return render_template("login.html", errors_json=[])
        else:  # If input has error
            return render_template("login.html", errors_json=json.dumps(form.errors))
    else:
        return render_template("login.html", errors_json=[])
    
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')
"""