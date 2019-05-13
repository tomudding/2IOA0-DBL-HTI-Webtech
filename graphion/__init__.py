"""
Author(s): Tom Udding
Created: 2019-04-29
Edited: 2019-05-05
"""
from flask import Flask
server = Flask(__name__)

# server needs to be defined before importing everything else
from asyncio import set_event_loop, new_event_loop
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from os import mkdir
from os.path import isdir
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

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
from graphion.selection import selectionBlueprint
from graphion.visualise import visualiseBlueprint

# register views as blueprints
server.register_blueprint(indexBlueprint)
server.register_blueprint(selectionBlueprint)
server.register_blueprint(visualiseBlueprint)

# other stuff
if (not isdir(server.config['UPLOAD_FOLDER'])):
    mkdir(server.config['UPLOAD_FOLDER'])

# start Bokeh server
sockets, port = bind_sockets("localhost", 0)
server.config['PORT'] = port

from graphion.visualise import modify_doc
bkapp = Application(FunctionHandler(modify_doc))

def bk_worker():
    set_event_loop(new_event_loop())

    bokeh_tornado = BokehTornado({'/bkapp': bkapp}, extra_websocket_origins=["localhost:5000"])
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()