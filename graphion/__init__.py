"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-04-29
Edited: 2019-06-10
"""
from flask import Flask
server = Flask(__name__)

from os import environ, mkdir, makedirs
from os.path import isdir
if (not isdir('logs')):
    mkdir('logs')

import logging
logger = logging.getLogger('werkzeug')
if "gunicorn" not in environ.get("SERVER_SOFTWARE", ""):
    from sys import stdout
    stdoutHandler = logging.StreamHandler(stdout)
    stdoutHandler.setLevel(logging.INFO)
    logger.addHandler(stdoutHandler)

if "gunicorn" not in environ.get("SERVER_SOFTWARE", ""):
    fileHandler = logging.FileHandler('logs/flask.log', mode="w")
else:
    fileHandler = logging.FileHandler('logs/flask.log')
fileHandler.setLevel(logging.INFO)
logger.addHandler(fileHandler)

# server needs to be defined before importing everything else
from asyncio import set_event_loop, new_event_loop
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from os import getpid
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# constants
SECRET_KEY = "2718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427"
SEED = 2464195387
UPLOAD_FOLDER = 'uploads'               #
TOKEN_SIZE = 16                         #
BUFFER_SIZE = 100000                    #
MAX_CONTENT_LENGTH = 1000 * 1024 * 1024 # limit file upload size to 1 GB

# app configurations
server.config['SECRET_KEY'] = SECRET_KEY
server.config['SEED'] = SEED
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['TOKEN_SIZE'] = TOKEN_SIZE
server.config['BUFFER_SIZE'] = BUFFER_SIZE
server.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# general imports
import graphion.error
import graphion.upload

# import views from app
from graphion.index import indexBlueprint
from graphion.selection import selectionBlueprint
from graphion.visualise import visualiseBlueprint
from graphion.filter import filterBlueprint
from graphion.api.filter.distribution import apiDegreeBlueprint
from graphion.api.visualise.plot_switching import apiSwitchBlueprint
from graphion.api.visualise.matrix_reordering import apiOrderBlueprint
from graphion.api.visualise.matrix_metric import apiMetricBlueprint
from graphion.api.visualise.matrix_palette import apiPaletteBlueprint

# register views as blueprints
server.register_blueprint(indexBlueprint)
server.register_blueprint(selectionBlueprint)
server.register_blueprint(visualiseBlueprint)
server.register_blueprint(filterBlueprint)
server.register_blueprint(apiDegreeBlueprint)
server.register_blueprint(apiSwitchBlueprint)
server.register_blueprint(apiOrderBlueprint)
server.register_blueprint(apiMetricBlueprint)
server.register_blueprint(apiPaletteBlueprint)

# other stuff
if (not isdir(server.config['UPLOAD_FOLDER'])):
    mkdir(server.config['UPLOAD_FOLDER'])

# start Bokeh server
if "gunicorn" in environ.get("SERVER_SOFTWARE", ""):
    forcedPort = getpid()
    sockets, port = bind_sockets("localhost", forcedPort)
    server.config['PORT'] = port + 20
    server.logger.info("STARTED LISTENING INTERNALLY ON %d AND EXTERNALLY ON %d" % (port, server.config['PORT']))
else:
    sockets, port = bind_sockets("localhost", 0)
    server.config['PORT'] = port

from graphion.visualise import modify_doc
bkapp = Application(FunctionHandler(modify_doc))

def bk_worker():
    set_event_loop(new_event_loop())

    bokeh_tornado = BokehTornado({'/bkapp': bkapp}, extra_websocket_origins=["localhost:5000", "graphion.uddi.ng:*"])
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()