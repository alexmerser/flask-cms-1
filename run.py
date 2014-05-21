#!/usr/bin/env python

#Create super user
#from tools.user import create_super_admin
#create_super_admin() 

from routes import index, post
from server import app

app.run()
