"""
Author(s): Steven van den Broek, Yuqin Cui
Created: 2019-05-05
Edited: 2019-05-05
"""
import numpy as np
import pandas as pd
import panel as pn
import param
import hvplot.pandas
from colorcet import palette
from scipy.spatial.distance import pdist, squareform
from fastcluster import linkage

# Graphion imports
from graphion.graphing.parser import processCSVMatrix

def makeMatrix(file):
    df = processCSVMatrix(file)
    names = df.columns.tolist()
    df = df.head(150)[names[0:150]]
    names = df.columns.tolist()
    names = [name.replace('_', ' ') for name in names]
    df.columns = names
    #convert similarity into unsimilarity (1.0 - similarity)
    for name in names:
        df[name] = 1 - df[name]
    #df.head()

    #This is just the method online: https://gmarti.gitlab.io/ml/2017/09/07/how-to-sort-distance-matrix.html
    #We have to clean data and modified the method

    dist_mat = squareform(pdist(df))

    def seriation(Z,N,cur_index):
        '''
            input:
                - Z is a hierarchical tree (dendrogram)
                - N is the number of points given to the clustering process
                - cur_index is the position in the tree for the recursive traversal
            output:
                - order implied by the hierarchical tree Z

            seriation computes the order implied by a hierarchical tree (dendrogram)
        '''
        if cur_index < N:
            return [cur_index]
        else:
            left = int(Z[cur_index-N,0])
            right = int(Z[cur_index-N,1])
            return (seriation(Z,N,left) + seriation(Z,N,right))

    def compute_serial_matrix(dist_mat,method="ward"):
        '''
            input:
                - dist_mat is a distance matrix
                - method = ["ward","single","average","complete"]
            output:
                - seriated_dist is the input dist_mat,
                  but with re-ordered rows and columns
                  according to the seriation, i.e. the
                  order implied by the hierarchical tree
                - res_order is the order implied by
                  the hierarhical tree
                - res_linkage is the hierarhical tree (dendrogram)

            compute_serial_matrix transforms a distance matrix into
            a sorted distance matrix according to the order implied
            by the hierarchical tree (dendrogram)
        '''
        N = len(dist_mat)
        flat_dist_mat = squareform(dist_mat)
        res_linkage = linkage(flat_dist_mat, method=method,preserve_input=True)
        res_order = seriation(res_linkage, N, N + N-2)
        seriated_dist = np.zeros((N,N))
        a,b = np.triu_indices(N,k=1)
        seriated_dist[a,b] = dist_mat[ [res_order[i] for i in a], [res_order[j] for j in b]]
        seriated_dist[b,a] = seriated_dist[a,b]

        return seriated_dist, res_order, res_linkage

    ordered_dist_mat = {}
    ordered_dist_mat['ward'], res_order, res_linkage = compute_serial_matrix(dist_mat,"ward")
    ordered_dist_mat['single'], res_order, res_linkage = compute_serial_matrix(dist_mat,"single")
    ordered_dist_mat['average'], res_order, res_linkage = compute_serial_matrix(dist_mat,"average")
    ordered_dist_mat['complete'], res_order, res_linkage = compute_serial_matrix(dist_mat,"complete")

    pn.extension()

    class Matrix_dropdown(param.Parameterized):
        reordering = param.ObjectSelector(default="ward",objects=["ward","single","average","complete"])

        def view(self):
            solid = pd.DataFrame(ordered_dist_mat[self.reordering])
            solid.index = names
            solid.columns = names
            solid.reset_index(inplace=True)
            liquid = solid.melt(id_vars='index', value_vars=list(df.columns[1:]), var_name="name2")
            liquid.columns = ['name1', 'name2', 'distance']
            return liquid.hvplot.heatmap('name1', 'name2', 'distance',
                          height=500, width=600, flip_yaxis=True, xaxis=None, yaxis=None, cmap=palette['kbc'])

    matrix = Matrix_dropdown(name='Adjacency Matrix')
    return pn.Column(matrix.param, matrix.view).get_root()
