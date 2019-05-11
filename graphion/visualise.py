"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-05-06
"""

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Blueprint, redirect, render_template
from graphion.graphing.generator import generateBokehApp
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
import asyncio

visualiseBlueprint = Blueprint('visualiseBlueprint', __name__, template_folder='templates')

@visualiseBlueprint.route('/visualise', methods=['GET'], strict_slashes=False)
@visualiseBlueprint.route('/visualise/<file>', methods=['GET'], strict_slashes=False)

def visualise(file=None):
    if file is None:
        return redirect('/selection')
    global file_global
    file_global = file
    script = server_document('http://localhost:%d/bkapp' % port, relative_urls=False, resources=None)
    return render_template('visualise.html', fileName=file, script=script)

def modify_doc(doc):
    doc.add_root(generateBokehApp(doc, file_global))

bkapp = Application(FunctionHandler(modify_doc))

sockets, port = bind_sockets("localhost", 0)

def bk_worker():
    asyncio.set_event_loop(asyncio.new_event_loop())

    bokeh_tornado = BokehTornado({'/bkapp': bkapp}, extra_websocket_origins=["localhost:5000"])
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()