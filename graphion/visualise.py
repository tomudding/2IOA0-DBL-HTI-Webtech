"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-06-08
"""
from flask import Blueprint, flash, redirect, render_template, request
from graphion import server
from graphion.graphing.generator import generateBokehApp
from graphion.upload import get_filtered_df
from bokeh.embed import server_document
import os
import time

visualiseBlueprint = Blueprint('visualiseBlueprint', __name__, template_folder='templates')

@visualiseBlueprint.route('/visualise', methods=['GET'], strict_slashes=False)
@visualiseBlueprint.route('/visualise/<file>', methods=['GET'], strict_slashes=False)
def visualise(file):
    if get_filtered_df() is None or get_filtered_df().size == 0:
        if file is None:
            flash("No dataset has been selected. Please select a previously uploaded dataset or upload a new dataset.", "danger")
            return redirect("/selection")
        else:
            return redirect("/filter/%s" % file)

    if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
        script = server_document('https://2ioa0.uddi.ng:%d/bkapp' % server.config['PORT'], relative_urls=False, resources=None, arguments={'sid': request.cookies.get(server.config['SESSION_COOKIE_NAME'])})
    else:
        script = server_document('http://localhost:%d/bkapp' % server.config['PORT'], relative_urls=False, resources=None, arguments={'sid': request.cookies.get(server.config['SESSION_COOKIE_NAME'])})
    return render_template('visualise.html', fileName=file, script=script)

def modify_doc(doc):
    begin = time.time()
    doc.add_root(generateBokehApp(doc))
    print("------------------------------------")
    print("Generating bokeh app in total: " + str(time.time() - begin))
    print()