"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-12
"""
from graphion import server
from graphion.graphing.linking import SelectEdgeCallback, SelectMatrixToNodeCallback, SelectNodeToMatrixCallback
from graphion.graphing.linking import SelectEdgeLink, SelectMatrixToNodeLink, SelectNodeToMatrixLink
from graphion.session.handler import get_custom_key, set_custom_key, get_filtered_df, set_screen1, get_screen1, \
    set_screen2, get_screen2, populate_3d_diagram, populate_force_diagram, populate_hierarchical_diagram,\
    populate_matrix, populate_radial_diagram, get_visualisations_app, set_visualisations_app, reset_plots, \
    get_matrix_df, get_datashading
import os
import panel as pn
import time

from bokeh.themes.theme import Theme

import param
import holoviews as hv

def generateBokehApp(doc):
    sid = str(doc.session_context.request.arguments['sid'][0].decode('utf-8'))
    reset_plots(sid)
    # Set theme for holoviews plots
    theme = Theme(
        json={
            'attrs': {
                'Figure': {
                    'background_fill_color': None,
                    'border_fill_color': None,
                    'outline_line_color': None,
                },
                'Grid': {
                    'grid_line_dash': [6, 4],
                    'grid_line_alpha': .3,
                },

                'Axis': {
                    'major_label_text_color': 'black',
                    'axis_label_text_color': 'black',
                    'major_tick_line_color': 'black',
                    'minor_tick_line_color': 'black',
                    'axis_line_color': "black"
                },

                'ColorBar': {
                    'background_fill_color': None,
                },

                'Nodes': {
                    'hover_fill_color': 'green',
                },

                'Points': {
                    'hover_fill_color': 'green',
                },

                'Graph': {
                    'hover_fill_color': 'green',
                }
            }
        })
    hv.renderer('bokeh').theme = theme


    class VisApp(param.Parameterized):
        Screen1 = param.ObjectSelector(default="force",
                                       objects=["none", "radial", "force", "hierarchical", "3d"])

        Screen2 = param.ObjectSelector(default="matrix",
                                       objects=["none", "matrix"])

        Ordering = param.ObjectSelector(default="none",
                                        objects=["none", "single", "average", "complete", "centroid", "weighted",
                                                 "median", "ward"])

        Metric = param.ObjectSelector(default="euclidean",
                                      objects=["euclidean", "minkowski", "cityblock", "sqeuclidean", "cosine",
                                               "correlation", "hamming", "jaccard", "chebyshev", "canberra",
                                               "braycurtis"])

        Color_palette = param.ObjectSelector(default='kbc',
                                             objects=['kbc', 'kgy', 'bgy', 'bmw', 'bmy', 'cividis', 'dimgray', 'fire',
                                                      'inferno', 'viridis'])
        Node_size = param.ObjectSelector(default='totalweight', 
                                            objects=['indegree', 'outdegree', 'totaldegree', 'inweight', 'outweight', 'totalweight'])

        Node_color = param.ObjectSelector(default='totalweight', 
                                            objects=['indegree', 'outdegree', 'totaldegree', 'inweight', 'outweight', 'totalweight'])

        def __init__(self, datashaded = True):
            self.datashaded = datashaded

            super(VisApp, self).__init__()

        @param.depends('Screen1', 'Screen2', 'Ordering', 'Metric', 'Color_palette', 'Node_size', 'Node_color')
        def view(self):
            print("Detected change in attributes")
            if self.Screen1 == "radial":
                set_screen1("radial", sid)
                populate_radial_diagram(df, sid, datashaded=self.datashaded)
            if self.Screen1 == "force":
                set_screen1("force", sid)
                populate_force_diagram(df, sid, datashaded=self.datashaded)
            if self.Screen1 == "hierarchical":
                set_screen1("hierarchical", sid)
                populate_hierarchical_diagram(df, sid, datashaded=self.datashaded)
            if self.Screen1 == "3d":
                set_screen1("3d", sid)
                populate_3d_diagram(df, sid)
            # print(s1[1])
            if self.Screen2 == "matrix":
                set_screen2("matrix", sid)
                populate_matrix(get_matrix_df(sid), sid)
                screen2 = get_custom_key(get_screen2(sid), sid)
                screen2.reordering = self.Ordering
                screen2.metric = self.Metric
                screen2.color_palette = self.Color_palette
                set_custom_key(get_screen2(sid), screen2, sid)

            # Setting up the linking, generateDiagram functions return two-tuple (graph, points). Points is the selection layer
            # makeMatrix returns matrix_dropdown object. matrix.view returns the heatmap object
            #SelectMatrixToNodeLink.register_callback('bokeh', SelectMatrixToNodeCallback)
            #SelectEdgeLink.register_callback('bokeh', SelectEdgeCallback)
            #SelectNodeToMatrixLink.register_callback('bokeh', SelectNodeToMatrixCallback)

            # Link matrix to the nodelink (both graph and points)
            #SelectMatrixToNodeLink(s2.view, s1[1])
            #SelectEdgeLink(s2.view, s1[0])

            # Link nodelink to matrix (points only)
            #SelectNodeToMatrixLink(s1[1], s2.view)
            gridSpec = pn.GridSpec(sizing_mode='stretch_both')

            if self.Screen1 == "3d":
                gridSpec[0, 0] = pn.Column(get_custom_key(get_screen1(sid), sid), css_classes=['screen-1', 'col-s-6'])
            else:
                screen1 = get_custom_key(get_screen1(sid), sid)
                screen1.color_palette = self.Color_palette
                screen1.node_size = self.Node_size
                screen1.node_color = self.Node_color
                set_custom_key(get_screen1(sid), screen1, sid)
                gridSpec[0, 0] = pn.Column(get_custom_key(get_screen1(sid), sid).view, css_classes=['screen-1', 'col-s-6'])

            gridSpec[0, 1] = pn.Column(get_custom_key(get_screen2(sid), sid).view, css_classes=['screen-2', 'col-s-6'])
            return gridSpec

    df = get_filtered_df(sid)

    #visApp = VisApp(datashaded=False)
    visApp = VisApp(datashaded=get_datashading(sid))

    set_visualisations_app(visApp, sid)

    # begin = time.time()
    # m = populate_matrix(df)
    # print("Matrix generation took: " + str(time.time()-begin))
    # begin = time.time()
    # h = populate_hierarchical_diagram(df)
    # print("Graph generation took: " + str(time.time()-begin))
    # begin = time.time()
    # threeD = populate_3d_diagram(df)
    # print("3D generation took: " + str(time.time() - begin))

    # pane = pn.Column(pn.Row(graph, matrix), graph3D)
    # pane = pn.Column(pn.Row(h, m), threeD)
    # pane = pn.Pane(graph)

    pn.extension('plotly')
    # Don't use pn.Pane since that messes up linking
    return pn.Column(visApp.view).get_root(doc)

def changeScreen1(new_type, sid):
    visApp = get_visualisations_app(sid)
    visApp.Screen1 = new_type
    set_visualisations_app(visApp, sid)

def changeOrdering(new_ordering, sid):
    visApp = get_visualisations_app(sid)
    visApp.Ordering = new_ordering
    set_visualisations_app(visApp, sid)

def changeMetric(new_metric, sid):
    visApp = get_visualisations_app(sid)
    visApp.Metric = new_metric
    set_visualisations_app(visApp, sid)

def changePalette(new_palette, sid):
    visApp = get_visualisations_app(sid)
    visApp.Color_palette = new_palette
    set_visualisations_app(visApp, sid)

def changeNodeSize(new_size, sid):
    visApp = get_visualisations_app(sid)
    visApp.Node_size = new_size
    print("Applying node sizes")
    set_visualisations_app(visApp, sid)
    print("Set node sizes..?")

def changeNodeColor(new_color, sid):
    visApp = get_visualisations_app(sid)
    visApp.Node_color = new_color
    print("Applying node colors")
    set_visualisations_app(visApp, sid)
    print("Set node colors..?")