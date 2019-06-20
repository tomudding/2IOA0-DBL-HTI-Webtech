"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-05-18
Edited: 2019-06-19
"""
from flask import Blueprint, flash, redirect, render_template, session, request
from graphion import server
from bokeh.embed import server_document
from graphion.graphing.parser import processCSVMatrix
from graphion.session.handler import set_df, is_user_loaded, prune_user, reset_dataframes, set_directed
from graphion.filtering.filter_dataframe import getGraphInfo
from os.path import exists, join
from pandas import read_hdf

filterBlueprint = Blueprint('filterBlueprint', __name__, template_folder='templates')

@filterBlueprint.route('/filter', methods=['GET'], strict_slashes=False)
@filterBlueprint.route('/filter/<file>', methods=['GET'], strict_slashes=False)
def visualise(file=None):
    if session.get("active", None) is None:
        session['active'] = True
        return redirect('/filter/%s' % file)

    if file is None:
        flash("No dataset has been selected. Please select a previously uploaded dataset or upload a new dataset.", "danger")
        return redirect('/selection')

    if not(exists(join(server.config['UPLOAD_FOLDER'], (file + '.h5')))):
        flash("Dataset could not be found. Please select a previously uploaded dataset or upload a new dataset.", "danger")
        return redirect('/selection')

    df = read_hdf(join(server.config['UPLOAD_FOLDER'], (file + '.h5'))) # this is the only and fastest way to do this with a fixed HDF format
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    if is_user_loaded(sid):
        prune_user(sid)
    set_df(df, file, sid)
    reset_dataframes(sid)

    # Get info
    nodes, edges, density, directed = getGraphInfo(df)

    # Save directedness in session
    set_directed(directed, sid)

    # Round and make percentage
    density = round(density * 100, 2)

    if directed:
        directedness = "directed"
    else:
        directedness = "undirected"
    return render_template('filter.html', fileName=file, nodes=nodes, edges=edges, sparcity=density, directedness=directedness)