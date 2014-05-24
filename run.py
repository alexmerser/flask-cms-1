#!/usr/bin/env python

#Create super user
#from tools.user import create_super_admin
#create_super_admin() 

from routes import index, item, address
from server import app

app.run()
