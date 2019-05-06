"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-01
"""
from flask import Blueprint, redirect, render_template
from graphion.graphing.generator import generateNodeLinkGraph, generateMatrix

testvisualiseBlueprint = Blueprint('testvisualiseBlueprint', __name__, template_folder='templates')

@testvisualiseBlueprint.route('/testvis', methods=['GET'], strict_slashes=False)
@testvisualiseBlueprint.route('/testvis/<file>', methods=['GET'], strict_slashes=False)
def visualise(file=None):
    if file is None:
        return redirect('/selection')
    return render_template('nodelink/forcedirected.html', fileName=file)
