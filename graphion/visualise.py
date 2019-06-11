"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-06-10
"""
from flask import Blueprint, flash, redirect, render_template, request, session
from graphion import server
from graphion.graphing.generator import generateBokehApp
from graphion.session.handler import get_filtered_df, is_global, is_user_loaded, set_matrix_df
from bokeh.embed import server_document
import os
import time

visualiseBlueprint = Blueprint('visualiseBlueprint', __name__, template_folder='templates')

@visualiseBlueprint.route('/visualise', methods=['GET'], strict_slashes=False)
@visualiseBlueprint.route('/visualise/<file>', methods=['GET'], strict_slashes=False)
def visualise(file):
    if session.get("active", None) is None:
        session['active'] = True
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    if not(is_global()) or not(is_user_loaded(sid)):
        if file is None:
            return redirect("/selection")
        else:
            return redirect("/filter/%s" % file)
    if get_filtered_df(sid) is None or get_filtered_df(sid).size == 0:
        if file is None:
            flash("No dataset has been selected. Please select a previously uploaded dataset or upload a new dataset.", "danger")
            return redirect("/selection")
        else:
            return redirect("/filter/%s" % file)

    # Set the dataframe with edges for the matrix
    set_matrix_df(sid)

    if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
        script = server_document('https://graphion.uddi.ng:%d/bkapp' % server.config['PORT'], relative_urls=False, resources=None, arguments={'sid': sid})
    else:
        script = server_document('http://localhost:%d/bkapp' % server.config['PORT'], relative_urls=False, resources=None, arguments={'sid': sid})
    return render_template('visualise.html', fileName=file, script=script)

def modify_doc(doc):
    begin = time.time()
    doc.add_root(generateBokehApp(doc))
    print("------------------------------------")
    print("Generating bokeh app in total: " + str(time.time() - begin))
    print()