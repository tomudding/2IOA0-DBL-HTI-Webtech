import numpy as np

adj_matrix = np.array([[5, 2, 3, 20],[9, 4, 6, 122], [7,13,16, 55], [45, 66, 77, 88]])

print(adj_matrix)
del_lst = [0, 2]
#del_lst = [i - del_lst_temp.index(i) for i in del_lst_temp]
print(del_lst)
b = np.delete(adj_matrix, (0, 1), axis = 0)

c = np.delete(adj_matrix, tuple(del_lst), 0)
d = np.delete(c, tuple(del_lst), 1)

print(b)
print(d)
