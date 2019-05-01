"""
Author(s): Tom Udding
Created: 2019-04-29
Edited: 2019-05-01
"""
import os
from flask import Flask
server = Flask(__name__)

# constants
UPLOAD_FOLDER = 'uploads'               #
ALLOWED_EXTENSIONS = set(['csv'])       #
BUFFER_SIZE = 64000                     #
MAX_CONTENT_LENGTH = 2 * 1024 * 1024    # limit file upload size to 2 MB

# app configurations
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# general imports
import app.error
import app.upload

# import views from app
from app.index import indexBlueprint
from app.visualise import visualiseBlueprint

# register views as blueprints
server.register_blueprint(indexBlueprint)

# other stuff
if (not os.path.isdir(server.config['UPLOAD_FOLDER'])):
    os.mkdir(server.config['UPLOAD_FOLDER'])
