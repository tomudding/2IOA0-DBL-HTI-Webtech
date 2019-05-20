from csv import Sniffer
from pandas.core.frame import DataFrame
from pandas.core.reshape.concat import concat
from pandas.io.parsers import read_csv
from pandas import read_hdf,read_csv
import numpy as np
import pandas
import os
import numpy as np

def processCSVMatrix(file):
    with open(file, 'r') as csvfile:
        dialect = Sniffer().sniff(csvfile.readline())

    df = DataFrame()
    for chunk in read_csv(file, sep=dialect.delimiter, mangle_dupe_cols=True, index_col=False, chunksize=1000):
        df = concat([df, chunk], ignore_index=True)

    nodes = df.columns.values.tolist()
    nodes.pop(0)
    df["Unnamed: 0"] = nodes
    df = df.rename(columns={'Unnamed: 0': 'name'})
    df = df.set_index(keys='name')

    return df

def generate_selection(file, kind = "edge", cutoff_l = 0.2, cutoff_r = 10.0, keep_edges = False):
    df = processCSVMatrix(file)
    fileUniqueHash ='test1'
    df.to_hdf(os.path.join("../../datasets/", (fileUniqueHash + '.h5')), key=fileUniqueHash)
    df = read_hdf(os.path.join("../../datasets/", (fileUniqueHash + '.h5')))

    #if file is already in hdf format, apply the following read method
    print(df[-20:])
    #df = read_hdf(file)


    adj_matrix = df.to_numpy(copy = True)  #convert dataframe to numpy array for efficiency

    adj_matrix_copy = adj_matrix.copy(True) #make a deep copy of the adjacency matrix
    print(adj_matrix)
    names = df.columns.tolist()

    for name in names:
        print(name)

    ##print(df[:10])
    #count = 0
    #for row in df.itertuples():
    #    if count < 10:
    #          print(row)
    #    for i in range(len(row))[1:]:
    #        edge_w = row[i]
    #        if(edge_w < cutoff_l or edge_w > cutoff_r):
    #            row[i] = 0.0
    #    count = count + 1
    #print(df[-10:])


    #edge weight fitering
    #for all weights outside of the cutoff range, write its value to 0.0
    for i in range(len(adj_matrix)): #iterate through rows
        for j in range(len(adj_matrix[i])): #iterate through columns
            w = adj_matrix[i][j]
            if(w < cutoff_l or w > cutoff_r):
                adj_matrix_copy[i][j] = 0.0

    #print matrix after edge weights are filtered
    print(adj_matrix_copy)

    del_lst1 = []
    del_lst2 = []

    for m in range(len(adj_matrix_copy)):
        if sum(adj_matrix_copy[m]) - adj_matrix_copy[m][m] == 0.0: #node with index m has total out-degree 0
            #minus the diagonal component to remove self-connecting edges
            del_lst1.append(m)
    for n in range(len(adj_matrix_copy.transpose())):
        if sum(adj_matrix_copy[n]) - adj_matrix_copy[n][n] == 0.0: #node with index n has total in-degree 0
            #minus the diagonal component to remove self-connecting edges
            del_lst2.append(n)
    del_lst = intersection(del_lst1, del_lst2)
    #rem_lst = [ i in range[len(adj_matrix)] not in del_lst]

    print(del_lst1)
    print(del_lst2)
    print(del_lst)

    #below nodes in the del_lst will be deleted
    c = np.delete(adj_matrix, tuple(del_lst), 0)
    d = np.delete(adj_matrix_copy, tuple(del_lst), 0)
    filtered_node_matrix = np.delete(c, tuple(del_lst), 1)
    filtered_edge_node_matrix = np.delete(d, tuple(del_lst), 1)

    #test #########################
    print(adj_matrix[del_lst[3]][1])
    print(filtered_node_matrix[del_lst[3]][1])
    print(adj_matrix[2][del_lst[-1]])
    print(filtered_node_matrix[2][del_lst[-1]])
    print(filtered_node_matrix)
    print(filtered_edge_node_matrix)
    #################################

    if keep_edges:
        filtered_node_matrix
    return filtered_edge_node_matrix



def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3

generate_selection("../../datasets/GephiMatrix_author_similarity.csv")
