"""
Author(s): Tom Udding
Created: 2019-04-29
Edited: 2019-04-29
"""
from flask import Flask
server = Flask(__name__)

# general imports
import app.error

# import views from app
from app.index import indexBlueprint

# register views as blueprints
server.register_blueprint(indexBlueprint)
