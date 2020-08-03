import numpy as np

def time_matrix(M, T):
    r = []
    for i in M:
        tmp = []
        for j in T:
            tmp.append(j / i)
        r.append(tmp)
    return np.array(r)


def cost_matrix(time_matrix, K):
    m = []
    for i in range(len(time_matrix)):
        tmp = []
        for j in time_matrix[i]:
            tmp.append(K[i] * j)
        m.append(tmp)
    return m
