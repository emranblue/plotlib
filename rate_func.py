import numpy as np
from plotlib.constant import size

def sigmoid(x):
    return ((2/(1+np.exp(-x)))-1)*10

def linear(x):
    return x

def map_func_array(func,array):
    if callable(func):
        return np.array(list(map(func,np.array(array))),dtype=object)


def cairo_context_to_pixel_array(surface):
    return np.ndarray(shape=(surface.get_width(),surface.get_height(),4),dtype=np.uint8,buffer=surface.get_data())
    

def buffer_to_numpy_array(buf,width,height):
    return np.ndarray(shape=(width,height),dtype=np.uint8,buffer=buf)


def gcd(a,b):
    if b==0:
        return a
    return gcd(b,a%b)
    
    
def d2u_p(x,y):
    return gcd(*size)*x+int(size[0]/2),-gcd(*size)*y+int(size[1]/2)
    
    
def multiplyfunc(f1,f2):
        return lambda x:f1(x)*f2(x)
    
    
def return_polar(function):
        function_x=multiplyfunc(function,np.cos)
        function_y=multiplyfunc(function,np.sin)
        return [function_x,function_y]
    

def slow_down(n):
    return np.power(n,3)
    
    
def homotopy_func(f1,f2,alpha):
        return np.array([lambda x:(alpha)*f1[0](x)+(1-alpha)*f2[0](x),lambda x:(alpha)*f1[1](x)+(1-alpha)*f2[1](x)],dtype=object)
        
