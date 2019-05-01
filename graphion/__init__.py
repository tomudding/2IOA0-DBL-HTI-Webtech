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
TOKEN_SIZE = 16                         #
ALLOWED_EXTENSIONS = set(['csv'])       #
BUFFER_SIZE = 64000                     #
MAX_CONTENT_LENGTH = 20 * 1024 * 1024   # limit file upload size to 20 MB

# app configurations
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['TOKEN_SIZE'] = TOKEN_SIZE
server.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
server.config['BUFFER_SIZE'] = BUFFER_SIZE
server.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# general imports
import graphion.error
import graphion.upload

# import views from app
from graphion.index import indexBlueprint
from graphion.visualise import visualiseBlueprint

# register views as blueprints
server.register_blueprint(indexBlueprint)
server.register_blueprint(visualiseBlueprint)

# other stuff
if (not os.path.isdir(server.config['UPLOAD_FOLDER'])):
    os.mkdir(server.config['UPLOAD_FOLDER'])