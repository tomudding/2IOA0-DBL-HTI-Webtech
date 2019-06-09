"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-06-09
Edited: 2019-06-09
"""
def get_df(sid):
    if not('df' in app_context['data'][sid]):
        return None
    return app_context['data'][sid]['df'].copy()

def set_df(input, sid):
    if not('app_context' in globals()):
        global app_context
        app_context = {'sessions': {}, 'data': {}}
    if app_context['sessions'].get(sid, None) is None:
        app_context['sessions'][sid] = {}
        app_context['data'][sid] = {}
    app_context['data'][sid]['df'] = input
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
    if 'filtered_df' in app_context['data'][sid]:
        if app_context['data'][sid]['filtered_df'] is not None: # we should make it that this can never be None; it exists or it doesn't.
            return app_context['data'][sid]['filtered_df'].copy()
    if 'almost_filtered_df' in app_context['data'][sid]:
        if app_context['data'][sid]['almost_filtered_df'] is not None:
            return app_context['data'][sid]['almost_filtered_df'].copy()
    if 'partially_filtered_df' in app_context['data'][sid]:
        if app_context['data'][sid]['almost_filtered_df'] is not None:
            return app_context['data'][sid]['partially_filtered_df'].copy()
    return get_df(sid)

def set_filtered_df(input, sid):
    app_context['data'][sid]['filtered_df'] = input

def get_partially_filtered_df(sid):
    if 'partially_filtered_df' in app_context['data'][sid]:
        if app_context['data'][sid]['partially_filtered_df'] is not None:
            return app_context['data'][sid]['partially_filtered_df'].copy()
    return get_df(sid)

def set_partially_filtered_df(input, sid):
    app_context['data'][sid]['partially_filtered_df'] = input

def get_almost_filtered_df(sid):
    if 'almost_filtered_df' in app_context['data'][sid]:
        if app_context['data'][sid]['almost_filtered_df'] is not None:
            return app_context['data'][sid]['almost_filtered_df'].copy()
    return get_df(sid)

def set_almost_filtered_df(input, sid):
    app_context['data'][sid]['almost_filtered_df'] = input