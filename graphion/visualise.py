"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-05-06
"""
from flask import Blueprint, redirect, render_template
from graphion import server
from graphion.graphing.generator import generateBokehApp
from bokeh.embed import server_document

visualiseBlueprint = Blueprint('visualiseBlueprint', __name__, template_folder='templates')

@visualiseBlueprint.route('/visualise', methods=['GET'], strict_slashes=False)
@visualiseBlueprint.route('/visualise/<file>', methods=['GET'], strict_slashes=False)
def visualise(file=None):
    if file is None:
        return redirect('/selection')
    script = server_document('http://localhost:%d/bkapp' % server.config['PORT'], relative_urls=False, resources=None, arguments={'file': file})
    return render_template('visualise.html', fileName=file, script=script)

def modify_doc(doc):
    doc.add_root(generateBokehApp(doc))