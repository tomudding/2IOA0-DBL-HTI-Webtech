import numpy as np
import bisect
import itertools

import time

adj_matrix = np.array([[5, 2, 3, 20],[9, 4, 13, 122], [7, 13, 16, 55], [45, 66, 66, 88]])




arr = adj_matrix.flatten("C")   #flattens it to a 1-D numpy array
index, weight = np.argsort(arr), np.sort(arr)
length = len(weight)
dict = dict(zip(range(length),zip(index, weight)))
l = bisect.bisect_left(weight, 13)
r = bisect.bisect_right(weight, 66)
ans = list(itertools.repeat(0.0, length))
for x in range(l, r):
    i, w = dict[x]
    ans[i] = w
print(ans)


#print(i)
#m = adj_matrix.flatten("C")   #flattens it to a 1-D numpy array
#i, w = np.argsort(m), np.sort(m)
#l = bisect.bisect_left(w, 13)
#r = bisect.bisect_right(w, 66)
#ans = list(itertools.repeat(0.0, len(w)))
#for x in range(l, r):
#    ans[i[x]] = w[x]
#print(ans)


#e = list(itertools.repeat(0, l)) + w[l:r] + list(itertools.repeat(0, len(w)-r))
#print("i")
##j = np.argsort(i)
#print("j")
#print(j)
#ans = list(itertools.repeat(0, len(w)))
#for x in range(len(e)):
#    ans[j[x]] = e[x]
#print(ans)
#print(0);
#print(i)
#print(e)

#m.sort()
#l = bisect.bisect_left(m, 13)
#r = bisect.bisect_right(m, 66)
#s = m[l:r]
start = time.time()
m = adj_matrix.flatten("C").tolist()
print(m)
#for i in range(len(m)):
#    tup = (i, m[i])
#    m[i] = tup
#m = [[i, m[i]] for i in range(len(m))]
m = list(zip(range(len(m)),m))
print(m)

sortOne = lambda val:val[0]
sortSecond = lambda val:val[1]
m.sort(key = sortSecond) #0(nlogn)
print(m)

i, w = list(zip(*m))[0], list(zip(*m))[1]
print(i)
print(w)
l = bisect.bisect_left(w, 13)
r = bisect.bisect_right(w, 66)
print("!!!")

m1 = list(zip(i[:l], itertools.repeat(0.0, l))) + m[l:r] + list(zip(i[r:], itertools.repeat(0.0, len(m) - r)))
print(m1)
print(m)
m1.sort(key = sortOne)
#m1 = list(zip(*m1))[1]
print("!!!");
m1 = [tup[1] for tup in m1]
m = adj_matrix.flatten("C").tolist()
print(m)
print(m1)

print(l)
print(r)
print(w)

del_lst = [0, 2]
#del_lst = [i - del_lst_temp.index(i) for i in del_lst_temp]
print(del_lst)
b = np.delete(adj_matrix, (0, 1), axis = 0)

c = np.delete(adj_matrix, tuple(del_lst), 0)
d = np.delete(c, tuple(del_lst), 1)

print(b)
print(d)
