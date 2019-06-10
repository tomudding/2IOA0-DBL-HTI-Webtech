"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-09
"""
from graphion import server
from graphion.graphing.linking import SelectEdgeCallback, SelectMatrixToNodeCallback, SelectNodeToMatrixCallback
from graphion.graphing.linking import SelectEdgeLink, SelectMatrixToNodeLink, SelectNodeToMatrixLink
from graphion.session.handler import get_custom_key, set_custom_key, get_filtered_df, set_screen1, get_screen1, \
    set_screen2, get_screen2, populate_3d_diagram, populate_force_diagram, populate_hierarchical_diagram,\
    populate_matrix, populate_radial_diagram, get_visualisations_app, set_visualisations_app, reset_plots
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

        @param.depends('Screen1', 'Screen2', 'Ordering', 'Metric', 'Color_palette')
        def view(self):
            if self.Screen1 == "radial":
                set_screen1("radial", sid)
                populate_radial_diagram(df, sid)
            if self.Screen1 == "force":
                set_screen1("force", sid)
                populate_force_diagram(df, sid)
            if self.Screen1 == "hierarchical":
                set_screen1("hierarchical", sid)
                populate_hierarchical_diagram(df, sid)
            if self.Screen1 == "3d":
                set_screen1("3d", sid)
                populate_3d_diagram(df, sid)
            # print(s1[1])
            if self.Screen2 == "matrix":
                set_screen2("matrix", sid)
                populate_matrix(df, sid)
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

            if self.Screen1 == "3d":
                return pn.Row(get_custom_key(get_screen1(sid), sid), pn.Column(get_custom_key(get_screen2(sid), sid).view))

            screen1 = get_custom_key(get_screen1(sid), sid)
            screen1.color_palette = self.Color_palette
            set_custom_key(get_screen1(sid), screen1, sid)
            return pn.Row(get_custom_key(get_screen1(sid), sid).view, pn.Column(get_custom_key(get_screen2(sid), sid).view))

    df = get_filtered_df(sid)
    visApp = VisApp()
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
    return pn.Pane(visApp.view).get_root(doc)

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