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

def generate_edge_selection(file, kind = "edge", cutoff_l = 0.6, cutoff_r = 10.0, keep_edges = False):
    #if file is already in hdf format, apply the following read method
    df = read_hdf(file)
    # print(df[-20:])

    adj_matrix = df.to_numpy(copy = True)  #convert dataframe to numpy array for efficiency

    adj_matrix_copy = adj_matrix.copy(True) #make a deep copy of the adjacency matrix
    # print(adj_matrix)
    names = df.columns.tolist()

    #edge weight fitering
    #for all weights outside of the cutoff range, write its value to 0.0
    for i in range(len(adj_matrix)): #iterate through rows
        for j in range(len(adj_matrix[i])): #iterate through columns
            w = adj_matrix[i][j]
            if(w < cutoff_l or w > cutoff_r):
                adj_matrix_copy[i][j] = 0.0

    #print matrix after edge weights are filtered
    # print(adj_matrix_copy)

    del_lst1 = []
    del_lst2 = []

    for m in range(len(adj_matrix_copy)):
        # print(sum(adj_matrix_copy[m]))
        # print(adj_matrix_copy[m][m])
        if sum(adj_matrix_copy[m]) - adj_matrix_copy[m][m] == 0.0: #node with index m has total out-degree 0
            #minus the diagonal component to remove self-connecting edges
            del_lst1.append(m)
    for n in range(len(adj_matrix_copy.transpose())):
        if sum(adj_matrix_copy[n]) - adj_matrix_copy[n][n] == 0.0: #node with index n has total in-degree 0
            #minus the diagonal component to remove self-connecting edges
            del_lst2.append(n)
    del_lst = intersection(del_lst1, del_lst2)

    # print(del_lst1)
    # print(del_lst2)
    # print(del_lst)

    #below nodes in the del_lst will be deleted
    c = np.delete(adj_matrix, tuple(del_lst), 0)
    d = np.delete(adj_matrix_copy, tuple(del_lst), 0)
    filtered_node_matrix = np.delete(c, tuple(del_lst), 1)
    filtered_edge_node_matrix = np.delete(d, tuple(del_lst), 1)

    #test #########################
    # print(adj_matrix[del_lst[3]][1])
    # print(filtered_node_matrix[del_lst[3]][1])
    # print(adj_matrix[2][del_lst[-1]])
##  aprint(filtered_node_matrix[2][del_lst[-1]])
    # print(filtered_node_matrix)
    # print(filtered_edge_node_matrix)
    #################################

    rem_lst = [i for i in range(len(adj_matrix)) if i not in del_lst]  # remaining indices
    rem_names = [names[i] for i in rem_lst] # search and list the remaining column names with the remaining indices

    #build the output dataframes
    df_filtered_keep_edge = pandas.DataFrame(filtered_node_matrix, index = rem_names, columns = rem_names)
    df_filtered_not_keep_edge = pandas.DataFrame(filtered_edge_node_matrix, index = rem_names, columns = rem_names)


    if keep_edges:
        df_filtered_keep_edge
    return df_filtered_not_keep_edge


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def generate_degree_selection(file, cutoff_l = 2, cutoff_r = 900, dir = "in"):
    df = read_hdf(file)

    adj_matrix = df.to_numpy(copy=True)  # convert dataframe to numpy array for efficiency

    #print(adj_matrix)
    names = df.columns.tolist()

    # degree weight fitering

    del_lst = []  # initialize list of indices of nodes going to be deleted

    if dir == "out":
        # for all nodes with out-degree outside of the cutoff range, add them to the delete list
        for i in range(len(adj_matrix)):  # iterate through rows
            count = 0  #initialize the count for zero weights
            for j in range(len(adj_matrix[i])):  # iterate through columns
                if adj_matrix[i][j] == 0.0 and not i == j: #don't count the diagonal edge
                    count += 1
            out_degree = len(adj_matrix[i]) - count #outdegree equals to the remaining none zero columns in given row
            #print(out_degree)
            if(out_degree < cutoff_l or out_degree > cutoff_r):
                del_lst.append(i)


    elif dir == "in":
        # for all nodes with in-degree outside of the cutoff range, add them to the delete list
        adj_matrix_t = adj_matrix.transpose();
        for i in range(len(adj_matrix_t)):  # iterate through rows
            count = 0  # initialize the count for zero weights
            for j in range(len(adj_matrix_t[i])):  # iterate through columns
                if adj_matrix_t[i][j] == 0.0 and not i == j: #don't count the diagonal edge
                    count += 1

            in_degree = len(adj_matrix_t[i]) - count  # indegree equals to the remaining none zero columns in given row
            print(in_degree)
            if (in_degree < cutoff_l or in_degree > cutoff_r):
                del_lst.append(i)
    else:
        print("invalid dir value!")

    # print(del_lst)
    rem_lst = [i for i in range(len(adj_matrix)) if i not in del_lst]  # remaining indices
    rem_names = [names[i] for i in rem_lst]  # search and list the remaining column names with the remaining indices

    c = np.delete(adj_matrix, tuple(del_lst), 0)
    result_matrix = np.delete(c, tuple(del_lst), 1)

   #  print(result_matrix)

    # build the output dataframes
    output_df = pandas.DataFrame(result_matrix, index=rem_names, columns=rem_names)
    # print(output_df)

    return output_df, rem_names

#generate_edge_selection("../../datasets/GephiMatrix_author_similarity.csv")
