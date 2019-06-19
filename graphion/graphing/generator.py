"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-19
"""
from bokeh.themes.theme import Theme
from graphion import server
from graphion.graphing.linking import SelectEdgeCallback, SelectMatrixToNodeCallback, SelectNodeToMatrixCallback, \
     SelectNodeToTableCallback,  SelectEdgeLink, SelectMatrixToNodeLink, SelectNodeToMatrixLink, SelectNodeToTableLink
from graphion.session.handler import get_custom_key, set_custom_key, get_filtered_df, set_screen1, get_screen1, \
     set_screen2, get_screen2, populate_3d_diagram, populate_force_diagram, populate_hierarchical_diagram, \
     populate_matrix, populate_radial_diagram, get_visualisations_app, set_visualisations_app, reset_plots, \
     get_matrix_df, get_datashading
from holoviews import renderer, Table
from holoviews.plotting.bokeh.callbacks import LinkCallback
from holoviews.plotting.links import Link
from panel import Column, extension, GridSpec
from param import depends, ObjectSelector, Parameterized

def generateBokehApp(doc):
    sid = str(doc.session_context.request.arguments['sid'][0].decode('utf-8'))
    reset_plots(sid)

    df = get_filtered_df(sid)

    class SelectedDataLink(Link):
        _requires_target = True

    class SelectedDataCallback(LinkCallback):

        source_model = 'selected'
        source_handles = ['cds']
        on_source_changes = ['indices']

        target_model = 'cds'

        source_code = "let len = {}".format(len(df.columns)) + """
                    let new_indices = []
                    for (let i = 0; i < source_selected.indices.length; i++){
                        let index = source_selected.indices[i]
                        j = len-1-(index%len)+Math.floor(index/(len))*(len)
                        new_indices[i] = j
                    }
                    var inds = source_selected.indices
                    var d = source_cds.data

                    selected_data = {}
                    selected_data['index1'] = []
                    selected_data['index2'] = []
                    selected_data['value'] = []
                    selected_data['zvalues'] = []

                    for (var i = 0; i < inds.length; i++){
                        selected_data['index1'].push(d['index1'][inds[i]])
                        selected_data['index2'].push(d['index2'][inds[i]])
                        selected_data['value'].push(d['value'][inds[i]])
                        selected_data['zvalues'].push(d['zvalues'][inds[i]])
                    }
                    target_cds.data = selected_data

                """

    SelectedDataLink.register_callback('bokeh', SelectedDataCallback)



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
    renderer('bokeh').theme = theme
    renderer('bokeh').webgl = True

    class VisApp(Parameterized):
        Screen1 = ObjectSelector(default="force",
                                       objects=["none", "radial", "force", "hierarchical", "3d"])

        Screen2 = ObjectSelector(default="matrix",
                                       objects=["none", "matrix"])

        Ordering = ObjectSelector(default="none",
                                        objects=["none", "single", "average", "complete", "centroid", "weighted",
                                                 "median", "ward"])

        Metric = ObjectSelector(default="euclidean",
                                      objects=["euclidean", "minkowski", "cityblock", "sqeuclidean", "cosine",
                                               "correlation", "hamming", "jaccard", "chebyshev", "canberra",
                                               "braycurtis"])

        Color_palette = ObjectSelector(default='kbc',
                                             objects=['kbc', 'kgy', 'bgy', 'bmw', 'bmy', 'cividis', 'dimgray', 'fire',
                                                      'inferno', 'viridis'])
        Node_size = ObjectSelector(default='indegreesize', 
                                            objects=['indegreesize', 'outdegreesize', 'totaldegreesize', 'inweightsize', 'outweightsize', 'totalweightsize'])

        Node_color = ObjectSelector(default='totalweight', 
                                            objects=['indegree', 'outdegree', 'totaldegree', 'inweight', 'outweight', 'totalweight'])

        def __init__(self, datashaded = True):
            self.datashaded = datashaded

            super(VisApp, self).__init__()

        @depends('Screen1', 'Screen2', 'Ordering', 'Metric', 'Color_palette', 'Node_size', 'Node_color')
        def view(self):
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
            screen1 = get_custom_key(get_screen1(sid), sid)
            gridSpec = GridSpec(sizing_mode='stretch_both')

            if self.Screen1 == "3d":
                gridSpec[0, 0] = Column(get_custom_key(get_screen1(sid), sid), css_classes=['screen-1', 'col-s-6'])
            else:
                screen1.color_palette = self.Color_palette
                screen1.node_size = self.Node_size
                screen1.node_color = self.Node_color
                set_custom_key(get_screen1(sid), screen1, sid)

            if self.Screen2 == "matrix":
                set_screen2("matrix", sid)
                populate_matrix(get_matrix_df(sid), sid)
                screen2 = get_custom_key(get_screen2(sid), sid)
                screen2.reordering = self.Ordering
                screen2.metric = self.Metric
                screen2.color_palette = self.Color_palette
                set_custom_key(get_screen2(sid), screen2, sid)

                matrix = screen2.view()

                edge_table = Table(matrix.data)
                SelectedDataLink(matrix, edge_table)

                if self.Screen1 != "3d":
                    # Setting up the linking, generateDiagram functions return two-tuple (graph, points). Points is the selection layer
                    # makeMatrix returns matrix_dropdown object. matrix.view returns the heatmap object
                    SelectMatrixToNodeLink.register_callback('bokeh', SelectMatrixToNodeCallback)
                    SelectNodeToMatrixLink.register_callback('bokeh', SelectNodeToMatrixCallback)
                    SelectNodeToTableLink.register_callback('bokeh', SelectNodeToTableCallback)
                    graph, points = screen1.view()
                    node_table = Table(points.data[['index', 'indegree', 'outdegree']])
                    
                    # Link matrix to the nodelink (both graph and points)
                    SelectMatrixToNodeLink(matrix, points)
                    SelectNodeToTableLink(points, node_table)

                    # Link nodelink to matrix (points only)
                    SelectNodeToMatrixLink(points, matrix)
                    gridSpec[0, 0] = Column(graph * points, Column(node_table, css_classes=['node_table']),
                                               css_classes=['screen-1', 'col-s-6'])
                gridSpec[0, 1] = Column(matrix, Column(edge_table, css_classes=['edge_table']),
                                            css_classes=['screen-2', 'col-s-6'])

                # SelectedDataLink(matrix, points)
                # renderer = renderer('bokeh')
                # print(renderer.get_plot(points).handles)
            return gridSpec

    visApp = VisApp(datashaded=get_datashading(sid))
    set_visualisations_app(visApp, sid)

    extension('plotly')
    # Don't use pn.Pane since that messes up linking
    return Column(visApp.view).get_root(doc)

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
    set_visualisations_app(visApp, sid)

def changeNodeColor(new_color, sid):
    visApp = get_visualisations_app(sid)
    visApp.Node_color = new_color
    set_visualisations_app(visApp, sid)