"""
Author(s): Unknown
Created: Unknown
Edited 2019-06-19
"""
from bisect import bisect_left, bisect_right
from pandas.core.frame import DataFrame
from itertools import repeat
from numpy import array, argsort, asarray, concatenate, count_nonzero, delete, reshape, sort
from time import time

def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3

def fetch_edge_count(df, cutoff_l = 0.6, cutoff_r = 10.0):
    adj_matrix = df.to_numpy(copy=True)
    arr = adj_matrix.flatten("C")
    weight = sort(arr)
    l = bisect_left(weight, cutoff_l)
    r = bisect_right(weight, cutoff_r)
    return r - l;

def filter_df_weight(df, cutoff_l = 0.6, cutoff_r = 10.0):
    names = df.columns.tolist()
    width = len(names)
    adj_matrix = df.to_numpy(copy = True)  #convert dataframe to numpy array for efficiency

    #start = time()

    arr = adj_matrix.flatten("C")  # flattens it to a 1-D numpy array
    current = time()
    index, weight = argsort(arr), sort(arr)
    print(time() - current)
    length = len(weight)
    current = time()
    dict_x = dict(zip(range(length), zip(index, weight)))
    print("create dict")
    print(time() - current)
    l = bisect_left(weight, cutoff_l)
    r = bisect_right(weight, cutoff_r)

    ans = list(repeat(0.0, length))
    for x in range(l, r):
        i, w = dict_x[x]
        ans[i] = w

    ans_matrix = asarray(ans).reshape(width, width) #0.04630708694458008
    #print("convertbacktoMatrix")
    #convert back to df
    df_filtered = DataFrame(ans_matrix, index=names, columns=names)
    #print("convertbacktoDf")
    return df_filtered

def degree_bisect(arr, cutoff_l, cutoff_r):
    index, degree = argsort(arr), sort(arr)
    l = bisect_left(degree, cutoff_l)
    r = bisect_right(degree, cutoff_r)
    return concatenate((index[:l], index[r:]))

def generate_degree_selection(df, cutoff_l = 60, cutoff_r = 80, dir = "in"):
    # df = read_hdf(file)

    adj_matrix = df.to_numpy(copy=True)  # convert dataframe to numpy array for efficiency

    #print(adj_matrix)
    names = df.columns.tolist()

    # degree weight fitering

    del_lst = []  # initialize list of indices of nodes going to be deleted

    if dir == "out":
        output_lst = []
        # for all nodes with out-degree outside of the cutoff range, add them to the delete list
        for i in range(len(adj_matrix)):  # iterate through rows
            row = array(adj_matrix[i])
            # row = np.delete(row, i)

            ##count = 0  #initialize the count for zero weights
            ##for j in range(len(adj_matrix[i])):  # iterate through columns
            ##    if adj_matrix[i][j] == 0.0 and not i == j: #don't count the diagonal edge
            ##        count += 1
            ##out_degree = len(adj_matrix[i]) - 1 - count #outdegree equals to the remaining none zero columns in given row
            out_degree = count_nonzero(row)
            #print(out_degree)
            output_lst.append(out_degree)
            #if(out_degree < cutoff_l or out_degree > cutoff_r):
            #    del_lst.append(i)
        del_lst = degree_bisect(array(output_lst), cutoff_l, cutoff_r)


    elif dir == "in":
        output_lst = []
        # for all nodes with in-degree outside of the cutoff range, add them to the delete list
        adj_matrix_t = adj_matrix.transpose()
        for i in range(len(adj_matrix_t)):  # iterate through rows
            col = adj_matrix_t[i]
            # col = np.delete(col, i)
            #count = 0  # initialize the count for zero weights
            #for j in range(len(adj_matrix_t[i])):  # iterate through columns
            #    if adj_matrix_t[i][j] == 0.0 and not i == j: #don't count the diagonal edge
            #        count += 1

            #in_degree = len(adj_matrix_t[i]) - 1 - count  # indegree equals to the remaining none zero columns in given row

            in_degree = count_nonzero(col)
            #print(in_degree)
            output_lst.append(in_degree)
            #if (in_degree < cutoff_l or in_degree > cutoff_r):
            #    del_lst.append(i)
        del_lst = degree_bisect(array(output_lst), cutoff_l, cutoff_r)
    else:
        print("invalid dir value!")

    # print(del_lst)
    rem_lst = [i for i in range(len(adj_matrix)) if i not in del_lst]  # remaining indices
    rem_names = [names[i] for i in rem_lst]  # search and list the remaining column names with the remaining indices

    c = delete(adj_matrix, tuple(del_lst), 0)
    result_matrix = delete(c, tuple(del_lst), 1)

   #  print(result_matrix)

    # build the output dataframes
    output_df = DataFrame(result_matrix, index=rem_names, columns=rem_names)
    # print(output_df)
    return output_df


def generate_edge_selection(df, cutoff_l = 0.6, cutoff_r = 10.0, keep_edges = False):
    #if file is already in hdf format, apply the following read method
    # df = read_hdf(file)
    # print(df[-20:])
    #print(cutoff_l)
    #print(cutoff_r)
    adj_matrix = df.to_numpy(copy = True)  #convert dataframe to numpy array for efficiency

    adj_matrix_copy = adj_matrix.copy(True) #make a deep copy of the adjacency matrix
    #print(adj_matrix)
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
    c = delete(adj_matrix, tuple(del_lst), 0)
    d = delete(adj_matrix_copy, tuple(del_lst), 0)
    filtered_node_matrix = delete(c, tuple(del_lst), 1)
    filtered_edge_node_matrix = delete(d, tuple(del_lst), 1)

    #test #########################
    # print(adj_matrix[del_lst[3]][1])
    # print(filtered_node_matrix[del_lst[3]][1])
    # print(adj_matrix[2][del_lst[-1]])
##  aprint(filtered_node_matrix[2][del_lst[-1]])
    #print(filtered_node_matrix)
    #print(filtered_edge_node_matrix)
    #################################

    rem_lst = [i for i in range(len(adj_matrix)) if i not in del_lst]  # remaining indices
    rem_names = [names[i] for i in rem_lst] # search and list the remaining column names with the remaining indices

    #build the output dataframes
    df_filtered_keep_edge = DataFrame(filtered_node_matrix, index = rem_names, columns = rem_names)
    df_filtered_not_keep_edge = DataFrame(filtered_edge_node_matrix, index = rem_names, columns = rem_names)


    if keep_edges:
        return df_filtered_keep_edge
    return df_filtered_not_keep_edge