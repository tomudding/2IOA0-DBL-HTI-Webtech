"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-01
"""
from flask import Blueprint, redirect, render_template
from graphion.graphing.nodelink import createNodeLinkGraph

visualiseBlueprint = Blueprint('visualiseBlueprint', __name__, template_folder='templates')

@visualiseBlueprint.route('/visualise', methods=['GET'], strict_slashes=False)
@visualiseBlueprint.route('/visualise/<file>', methods=['GET'], strict_slashes=False)
def visualise(file=None):
    if file is None:
        return redirect('/selection')
    plots = []
    plots.append(createNodeLinkGraph(file))
    return render_template('visualise.html', fileName=file, plots=plots)