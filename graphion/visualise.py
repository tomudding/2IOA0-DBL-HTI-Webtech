"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-06-01
"""
from flask import Blueprint, redirect, render_template
from graphion import server
from graphion.graphing.generator import generateBokehApp
from graphion.upload import get_filtered_df
from bokeh.embed import server_document
import time

visualiseBlueprint = Blueprint('visualiseBlueprint', __name__, template_folder='templates')

@visualiseBlueprint.route('/visualise', methods=['GET'], strict_slashes=False)
def visualise():
    if get_filtered_df() is None:
        return redirect("/selection")

    script = server_document('http://localhost:%d/bkapp' % server.config['PORT'], relative_urls=False, resources=None)
    return render_template('visualise.html', script=script)

def modify_doc(doc):
    begin = time.time()
    doc.add_root(generateBokehApp(doc))
    print("------------------------------------")
    print("Generating bokeh app in total: " + str(time.time() - begin))
    print()