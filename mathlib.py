import numpy as np
from rate_func import d2u_p

ISO_PROJECT_METRIX=np.array([[1,-1,0],[1,1,1]])

def iso_project2plane(vector):
    global ISO_PROJECT_METRIX
    vector=np.array(vector)
    return np.matmul(ISO_PROJECT_METRIX,vector)


def all_iso_points(vectors):
    vectors=np.array(vectors)
    result=[]
    for vector in vectors:
        result.append(d2u_p(*iso_project2plane(vector)))
    return np.array(result)
