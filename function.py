from numpy import *
from plotlib.rate_func import linear
class PerametricFunction:
    def __init__(self,function):
        if function[0]:
            if callable(function[0]):
                self.passfunction_x(function[0])
            elif isinstance(function[0],str):
                self.setfunction_x(function[0])
        
        if function[1]:
            if callable(function[1]):
                self.passfunction_y(function[1])
            elif isinstance(function[1],str):
                self.setfunction_y(function[1])       
                
            
        
        
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
        #if isinstance(f1,) and isinstance(f2,list):
        return array([lambda x:(1-alpha)*f1[0](x)+alpha*f2[0](x),lambda x:(1-alpha)*f1[1](x)+alpha*f2[1](x)],dtype=object)
        

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
    def __init__(self,function):
        super.__init__(linear,function)
    
    #@classmethod    
    #def homotopy_func(cls,func,alpha):
        #return PerametricFunction.homotopy_func(linear,func,alpha)

class PolarFunction(Function):
    def __init__(self,function):
        if callable(function):
            self.function_x,self.function_y=[PerametricFunction.multiplyfunc(function,polar) for polar in [cos,sin]]
        elif isinstance(function,str):   
            self.function_x,self.function_y=PolarFunction.return_corresponding_polar(function)
        
    @classmethod
    def return_corresponding_polar(cls,func):
        function_x=PerametricFunction.multiplyfunc(PerametricFunction.functionaize(function),cos)
        function_y=PerametricFunction.multiplyfunc(PerametricFunction.functionaize(function),sin)
        return [function_x,function_y]
        
   
    #@classmethod
    #def homotopy_func(cls,func,alpha):
        #return PerametricFunction.homotopy_func(*PolarFunction.return_corresponding_polar(func),alpha)
        
        
       
       
       
   
   


