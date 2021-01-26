import numpy as np


def sigmoid(x):
    return (2/(1+np.exp(-x)))-1

def linear(x):
    return x

