#!/usr/bin/env python
#from core import myapp
#import controller.home

#import controller.user

#Create super user
#from tools.user import create_super_admin
#create_super_admin() 

from route import home
from server import app

app.run(debug = True)
