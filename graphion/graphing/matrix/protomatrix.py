"""
Author(s): Steven van den Broek, Yuqin Cui, Sam Baggen, Tom Udding
Created: 2019-05-05
Edited: 2019-06-06
"""
import numpy as np
import pandas as pd
import panel as pn
import param
from colorcet import palette
from flask import session
from scipy.spatial.distance import pdist, squareform
from fastcluster import linkage
from pandas import read_hdf
import time

import holoviews as hv
from holoviews.plotting.bokeh.callbacks import LinkCallback
from holoviews.plotting.links import Link
from bokeh.models import BoxSelectTool

from graphion.graphing.linking import SelectMatrixToNodeCallback, SelectMatrixToNodeLink

def makeMatrix(file, plot, df=False):
    if not df:
        df = read_hdf(file)
    else:
        df = file
    big_bang = time.time()
    names = df.columns.tolist()
    if (len(names) > 400):
        df = df.head(400)[names[0:400]]
    names = df.columns.tolist()
    names = [name.replace('_', ' ') for name in names]
    df.columns = names
    df.set_index([df.columns], inplace=True)

    df_original = df.copy()
    # %%
    # convert similarity into unsimilarity (1.0 - similarity)
    # begin = time.time()
    for name in names:
        df[name] = 1 - df[name]
    # print("Matrix, inverting values took: " + str(time.time()-begin))
    # %%
    # This is just the method online: https://gmarti.gitlab.io/ml/2017/09/07/how-to-sort-distance-matrix.html
    # We have to clean data and modified the method

    # %%
    # The output of linkage is stepwise dendrogram,
    # which is represented as an (N − 1) × 4 NumPy array with floating point entries (dtype=numpy.double).
    # The first two columns contain the node indices which are joined in each step. The input nodes are
    # labeled 0,..., N − 1, and the newly generated nodes have the labels N,...2N-2.
    # The third column contains the distance between the two nodes at each step, ie. the
    # current minimal distance at the time of the merge. The fourth column counts the
    # number of points which comprise each new node.

    # Idea is from: https://gmarti.gitlab.io/ml/2017/09/07/how-to-sort-distance-matrix.html

    # Traversal the hierarhical tree generated by linkage
    def traversal_tree(hier_tree, number_of_node, current_index):
        if current_index < number_of_node:
            return [current_index]
        else:
            return (traversal_tree(hier_tree, number_of_node, int(hier_tree[current_index - number_of_node][1])) +
                    traversal_tree(hier_tree, number_of_node, int(hier_tree[current_index - number_of_node][0])))

    # %%
    def compute_serial_matrix(df, method="ward", dist_metric="euclidean"):
        # define the dist_mat by different dist_metric mathod in fast_clustering package
        dist_mat = squareform(pdist(df, metric=dist_metric))
        # hierar tree was got from package "fast-clustering"
        hierar_tree = linkage(squareform(dist_mat), method=method, preserve_input=True)
        # The order implied by the hierarhical tree
        reordered_index = traversal_tree(hierar_tree, len(dist_mat), 2 * len(dist_mat) - 2)
        return reordered_index, hierar_tree

    # linkage(squareform(pdist(df, metric="euclidean")), method="ward",preserve_input=True)
    # %%
    # order original matrix based on index provided
    def author_reorder_list(df, order):
        new_names = df.columns
        return [new_names[i] for i in order]

    def reordercol(df, order):
        secondIndex = []
        new_df = df
        new_df['nindex'] = np.arange(len(new_df))
        for i in order:
            secondIndex += new_df.index[new_df['nindex'] == i].tolist()
        new_df.drop('nindex', axis=1, inplace=True)
        a = new_df.reindex(index=secondIndex)
        return a

    def reorderrow(df, order):
        a = df.values
        permutation = order
        return a[:, permutation]

    def reorder_input_df(df, order):
        reorder_col = reordercol(df, order)
        finish = reorderrow(reorder_col, order)
        return finish

    # %%
    def to_liquid(matrix):
        solid = pd.DataFrame(matrix)
        solid.index = names
        solid.columns = names
        solid.reset_index(inplace=True)
        liquid = solid.melt(id_vars='index', value_vars=list(df.columns[0:]), var_name="name2")
        liquid.columns = ['index2', 'index1', 'value']
        liquid = liquid[['index1', 'index2', 'value']]
        # print(liquid)
        return liquid

    # %%
    def to_liquid_2(matrix, df, order):
        solid = pd.DataFrame(matrix)
        name_list = author_reorder_list(df, order)
        # print(name_list)
        solid.index = name_list
        solid.columns = name_list
        solid.reset_index(inplace=True)
        liquid = solid.melt(id_vars='index', value_vars=list(name_list[0:]), var_name="name2")
        liquid.columns = ['index2', 'index1', 'value']
        liquid = liquid[['index1', 'index2', 'value']]
        # print(liquid)
        return liquid

    # %%
    def dis_to_similarity(grid):
        nrows = len(grid)
        ncols = len(grid[0])
        for i in range(nrows):
            for j in range(ncols):
                grid[i][j] = 1 - grid[i][j]
                # %%

    pn.extension()

    select_tool = BoxSelectTool()

    result = to_liquid(df_original.values)
    session['hm'] = hv.HeatMap(result).opts(tools=['tap', select_tool, 'hover'], active_tools=['box_select'],
                                 height=550, width=600, xaxis=None, yaxis=None, cmap=palette['kbc'])
    session['current_data'] = session['hm'].data

    class Matrix_dropdown(param.Parameterized):
        reordering = param.ObjectSelector(default="none",
                                          objects=["none", "single", "average", "complete", "centroid", "weighted",
                                                   "median", "ward"])
        metric = param.ObjectSelector(default="euclidean",
                                      objects=["euclidean", "minkowski", "cityblock", "sqeuclidean", "cosine",
                                               "correlation", "hamming", "jaccard", "chebyshev", "canberra",
                                               "braycurtis"])
        color_palette = param.ObjectSelector(default='kbc',
                                             objects=['kbc', 'kgy', 'bgy', 'bmw', 'bmy', 'cividis', 'dimgray', 'fire',
                                                      'inferno', 'viridis'])

        def view(self, show_only_selection=True):
            if self.reordering == "none":
                # if 'selection' in globals():
                #     selection.clear()

                result = to_liquid(df_original.values)
                # return result.hvplot.heatmap('index1', 'index2', 'value', invert=True, tools=['tap', select_tool],
                #          height=500, width=600, flip_yaxis=True, xaxis=None, yaxis=None, cmap=palette['kbc'])

                hm = hv.HeatMap(result).opts(tools=['tap', select_tool, 'hover'], toolbar='above', active_tools=['box_select'],
                                             height=500, width=530, xaxis=None, yaxis=None, cmap=self.color_palette,
                                             colorbar=True)
                session['current_data'] = session['hm'].data
                table = hv.Table(session['current_data'])
                table.opts(height=500)

                # print(plot)
                select = SelectMatrixToNodeLink(hm, plot, indices=names)
                select.register_callback('bokeh', SelectMatrixToNodeCallback)

                return session['hm']
                # return pn.Row(hm, table)
                # selection = Selection1D(source=hm, subscribers=[print_info])
                # return hv.DynamicMap(lambda index: hm, streams=[selection])
            else:
                #             if 'selection' in globals():
                #                 selection.clear()
                res_order, res_linkage = compute_serial_matrix(df, self.reordering, dist_metric=self.metric)
                reordered_matrix_col = reordercol(df, res_order)
                reordered_matrix = reorderrow(reordered_matrix_col, res_order)
                dis_to_similarity(reordered_matrix)
                # reordered_matrix = pd.DataFrame(reordered_matrix, index = author_reorder_list(df,res_order), column = author_reorder_list(df,res_order))
                result = to_liquid_2(reordered_matrix, df, res_order)
                hm = hv.HeatMap(result).opts(tools=['tap', select_tool, 'hover'], toolbar='above', active_tools=['box_select'],
                                             height=500, width=530, xaxis=None, yaxis=None, cmap=self.color_palette,
                                             colorbar=True)
                session['current_data'] = session['hm'].data
                table = hv.Table(session['current_data'])
                table.opts(height=500)
                # print(plot)
                select = SelectMatrixToNodeLink(hm, plot, indices=names)
                select.register_callback('bokeh', SelectMatrixToNodeCallback)


                return session['hm']
                # return pn.Row(hm, table)
                # selection = Selection1D(source=hm, subscribers=[print_info])
                # return hv.DynamicMap(lambda index: hm, streams=[selection])

    matrix = Matrix_dropdown(name='Adjacency Matrix')


    # %%
    # hv_plot = hm + table

    #matrix_pane1 = pn.Column(pn.Pane(matrix.param, css_classes=['matrix_dropdowns']), matrix.view)
    # matrix_pane2 = pn.Column(matrix.param, matrix.view(show_only_selection=False))

    return matrix