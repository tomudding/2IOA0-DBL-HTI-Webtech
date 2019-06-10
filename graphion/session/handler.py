"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-06-09
Edited: 2019-06-10
"""
from graphion.graphing.matrix.protomatrix import makeMatrix
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram, generateNodeLinkDiagram
from time import time

def is_global():
    global APP_CONTEXT
    if 'APP_CONTEXT' in globals():
        return True
    return False

def is_user_loaded(sid):
    global APP_CONTEXT
    if not(is_global()):
        return False
    if sid in APP_CONTEXT['data']:
        return True
    return False

def get_custom_key(key, sid):
    global APP_CONTEXT
    if not(key in APP_CONTEXT['data'][sid]):
        return None # we should raise KeyError
    return APP_CONTEXT['data'][sid][key]

def set_custom_key(key, value, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid][key] = value

def get_df(sid):
    global APP_CONTEXT
    if not('df' in APP_CONTEXT['data'][sid]):
        return None
    return APP_CONTEXT['data'][sid]['df'].copy()

def set_df(input, sid):
    if not(is_global()):
        global APP_CONTEXT
        APP_CONTEXT = {'sessions': {}, 'data': {}}
    if APP_CONTEXT['sessions'].get(sid, None) is None:
        APP_CONTEXT['sessions'][sid] = time() # store current time for when we want to prune the variable
        APP_CONTEXT['data'][sid] = {}
    APP_CONTEXT['data'][sid]['df'] = input

def get_filtered_df(sid):
    global APP_CONTEXT
    if 'filtered_df' in APP_CONTEXT['data'][sid]:
        if APP_CONTEXT['data'][sid]['filtered_df'] is not None: # we should make it that this can never be None; it exists or it doesn't.
            return APP_CONTEXT['data'][sid]['filtered_df'].copy()
    if 'almost_filtered_df' in APP_CONTEXT['data'][sid]:
        if APP_CONTEXT['data'][sid]['almost_filtered_df'] is not None:
            return APP_CONTEXT['data'][sid]['almost_filtered_df'].copy()
    if 'partially_filtered_df' in APP_CONTEXT['data'][sid]:
        if APP_CONTEXT['data'][sid]['almost_filtered_df'] is not None:
            return APP_CONTEXT['data'][sid]['partially_filtered_df'].copy()
    return get_df(sid)

def set_filtered_df(input, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['filtered_df'] = input

def get_partially_filtered_df(sid):
    global APP_CONTEXT
    if 'partially_filtered_df' in APP_CONTEXT['data'][sid]:
        if APP_CONTEXT['data'][sid]['partially_filtered_df'] is not None:
            return APP_CONTEXT['data'][sid]['partially_filtered_df'].copy()
    return get_df(sid)

def set_partially_filtered_df(input, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['partially_filtered_df'] = input

def get_almost_filtered_df(sid):
    global APP_CONTEXT
    if 'almost_filtered_df' in APP_CONTEXT['data'][sid]:
        if APP_CONTEXT['data'][sid]['almost_filtered_df'] is not None:
            return APP_CONTEXT['data'][sid]['almost_filtered_df'].copy()
    return get_df(sid)

def set_almost_filtered_df(input, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['almost_filtered_df'] = input

def set_left_weight(input, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['left_weight'] = input

def get_left_weight(sid):
    global APP_CONTEXT
    if not('left_weight' in APP_CONTEXT['data'][sid]):
        return None
    return APP_CONTEXT['data'][sid]['left_weight']

def set_right_weight(input, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['right_weight'] = input

def get_right_weight(sid):
    global APP_CONTEXT
    if not('right_weight' in APP_CONTEXT['data'][sid]):
        return None
    return APP_CONTEXT['data'][sid]['right_weight']

def set_screen1(input, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['screen1'] = input

def get_screen1(sid):
    global APP_CONTEXT
    if not('screen1' in APP_CONTEXT['data'][sid]):
        return None
    return APP_CONTEXT['data'][sid]['screen1']

def set_screen2(input, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['screen2'] = input

def get_screen2(sid):
    global APP_CONTEXT
    if not('screen2' in APP_CONTEXT['data'][sid]):
        return None
    return APP_CONTEXT['data'][sid]['screen2']

def populate_matrix(df, sid):
    global APP_CONTEXT
    if 'matrix' in APP_CONTEXT['data'][sid]:
        plot = APP_CONTEXT['data'][sid]['matrix']
        if plot is not None:
            return plot
    matrix = makeMatrix(df.copy(), get_custom_key(get_screen1(sid), sid), df=True)
    APP_CONTEXT['data'][sid]['matrix'] = matrix
    return matrix

def populate_hierarchical_diagram(df, sid):
    global APP_CONTEXT
    if 'hierarchical' in APP_CONTEXT['data'][sid]:
        plot = APP_CONTEXT['data'][sid]['hierarchical']
        if plot is not None:
            return plot
    # hierarchical = generateHierarchicalDiagram(df.copy(), False, df=True)
    hierarchical = generateNodeLinkDiagram(df.copy(), 'hierarchical')
    APP_CONTEXT['data'][sid]['hierarchical'] = hierarchical
    return hierarchical

def populate_3d_diagram(df, sid):
    global APP_CONTEXT
    if '3d' in APP_CONTEXT['data'][sid]:
        if  APP_CONTEXT['data'][sid]['3d'] is not None:
            return APP_CONTEXT['data'][sid]['3d']
    graph3D = generate3DDiagram(df.copy(), df=True)
    APP_CONTEXT['data'][sid]['3d'] = graph3D
    return graph3D

def populate_force_diagram(df, sid):
    global APP_CONTEXT
    if 'force' in APP_CONTEXT['data'][sid]:
        if APP_CONTEXT['data'][sid]['force'] is not None:
            return APP_CONTEXT['data'][sid]['force']
    # force = generateForceDirectedDiagram(df.copy(), False, df=True)
    force = generateNodeLinkDiagram(df.copy(), 'force')
    APP_CONTEXT['data'][sid]['force'] = force
    return force

def populate_radial_diagram(df, sid):
    global APP_CONTEXT
    if 'radial' in APP_CONTEXT['data'][sid]:
        if APP_CONTEXT['data'][sid]['radial'] is not None:
            return APP_CONTEXT['data'][sid]['radial']
    # radial = generateRadialDiagram(df.copy(), False, df=True)
    radial = generateNodeLinkDiagram(df.copy(), 'radial')
    APP_CONTEXT['data'][sid]['radial'] = radial
    return radial

def get_visualisations_app(sid):
    global APP_CONTEXT
    if not('visapp' in APP_CONTEXT['data'][sid]):
        return None
    return APP_CONTEXT['data'][sid]['visapp']

def set_visualisations_app(app, sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['visapp'] = app

def reset_plots(sid):
    global APP_CONTEXT
    APP_CONTEXT['data'][sid]['radial'] = None
    APP_CONTEXT['data'][sid]['force'] = None
    APP_CONTEXT['data'][sid]['hierarchical'] = None
    APP_CONTEXT['data'][sid]['3d'] = None
    APP_CONTEXT['data'][sid]['matrix'] = None
