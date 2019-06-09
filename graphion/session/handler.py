"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-06-09
Edited: 2019-06-09
"""
from time import time

def get_df(sid):
    global APP_CONTEXT
    if not('df' in APP_CONTEXT['data'][sid]):
        return None
    return APP_CONTEXT['data'][sid]['df'].copy()

def set_df(input, sid):
    if not('APP_CONTEXT' in globals()):
        global APP_CONTEXT
        APP_CONTEXT = {'sessions': {}, 'data': {}}
    if APP_CONTEXT['sessions'].get(sid, None) is None:
        APP_CONTEXT['sessions'][sid] = time() # store current time for when we want to prune the variable
        APP_CONTEXT['data'][sid] = {}
    APP_CONTEXT['data'][sid]['df'] = input
    # if df.equals(df.transpose()):
    #     directed = False
    # else:
    #     directed = True
    # print("This dataset is directed: " + str(directed))
    # if (df.astype(bool).sum(axis=0).sum())/(df.size) > 0.5:
    #     sparce = False
    # else:
    #     sparce = True
    # print("This dataset is sparce: " + str(sparce))

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