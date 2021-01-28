from numpy import *
from rate_func import linear
class PerametricFunction:
    def __init__(self,f1=None,f2=None):
        if f1 is not None and f2 is not None:
            self.function_x=PerametricFunction.functionaize(f1)
            self.function_y=PerametricFunction.functionaize(f2)
        self.function_x=f1
        self.function_y=f2
        
        
    @classmethod
    def functionaize(cls,function:str):
        '''make users provided function into python function
        example:
        functionaize('x**2') this return python function like
        def f(x):
            return x**2
        '''
        return lambda x:eval(function)
        
        
    @classmethod
    def multiplyfunc(cls,f1,f2):
        return lambda x:f1(x)*f2(x)
    

    @classmethod
    def homotopy_func(cls,f1,f2,alpha):
        return lambda x:(1-alpha)*eval(f1)+alpha*eval(f2)
        

    def setlimit(self,a,b):
        self.a=eval(a)
        self.b=eval(b)

    def getlimit(self):
        return self.a,self.b

    def getfunction_x(self):
        return self.function_x

    def getfunction_y(self):
        return self.function_y

    def setfunction_x(self,function:str):
        self.function_x=PerametricFunction.functionaize(function)

    def setfunction_y(self,function:str):
        self.function_y=PerametricFunction.functionaize(function)

    def setfunction(self,f1:str,f2:str):
        self.function_x=PerametricFunction.functionaize(f1)
        self.function_y=PerametricFunction.functionaize(f2)

    def passfunction_x(self,func):
        self.function_x=func

    def passfunction_y(self,func):
        self.function_y=func


    def passfunctions(self,function1,function2):
        self.function_x=function1
        self.function_y=function2

    def passfunction(self,function):
        self.function_y=function
        self.function_x=linear


    def getfunction(self):
        return self.function_x,self.function_y

class Function(PerametricFunction):
    def __init__(self,function:str):
        self.setfunction_y(function)
        self.passfunction_x(linear)

class PolarFunction(Function):
    def __init__(self,function:str):
        self.function_x=PerametricFunction.multiplyfunc(PerametricFunction.functionaize(function),cos)
        self.function_y=PerametricFunction.multiplyfunc(PerametricFunction.functionaize(function),sin)


