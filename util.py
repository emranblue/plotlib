import numpy as np
from numpy.ctypeslib import ndpointer
from file_tracker import FileManager
from config import digest_config
import cairo,os,sys
from function import PerametricFunction

class GraphingTool(FileManager,PerametricFunction):
    CONFIG={
        'ratio':120,#gcd(1920,1080)=120
        'step':0.01,
        'rgb':(0.8,.85,0.1),
        'x0':960,
        'y0':540,
        'width':1920,
        'height':1080,
        'llim':-960,
        'rlim':960,
        'ulim':540,
        'dlim':-540
    }
    def __init__(self,fmt,dir_name,file_name,**kwargs):       
        digest_config(self,kwargs)
        super().__init__(fmt,dir_name,file_name)

    def getsurface(self):
        return self.surface

    def getcontext(self):
        return self.ctx

    def __hline__(self,b):
        self.ctx.set_source_rgb(.2,.8,1)
        self.ctx.move_to(*self.d2u_p(self.llim,b))
        self.ctx.line_to(*self.d2u_p(self.rlim,b))
        self.ctx.set_line_width(2)
        self.ctx.stroke()

    def __vline__(self,a):
        self.ctx.set_source_rgb(.2,.8,1)
        self.ctx.move_to(*self.d2u_p(a,self.dlim))
        self.ctx.line_to(*self.d2u_p(a,self.ulim))
        self.ctx.set_line_width(2)
        self.ctx.stroke() 

    def setaxis(self):
        self.ctx.set_source_rgb(1,1,1)
        self.ctx.move_to(*self.d2u_p(self.llim,0))
        self.ctx.line_to(*self.d2u_p(self.rlim,0))
        self.ctx.move_to(*self.d2u_p(0,self.ulim))
        self.ctx.line_to(*self.d2u_p(0,self.dlim))
        self.ctx.set_line_width(5)
        self.ctx.stroke() 

    def setgrid(self):
        width=int((self.rlim-self.llim)/self.ratio)
        n=self.llim
        for i in range(2,width+1):
            n+=self.ratio
            self.__vline__(int(n/self.ratio))
        width=int((self.ulim-self.dlim)/self.ratio)
        self.__hline__(int(width/self.ratio))
        n=self.dlim
        for i in range(1,width+2):
            n+=self.ratio
            self.__hline__(int(n/self.ratio))


    def init_canvas(self):
        if self.fmt=='svg':
            surface=cairo.SVGSurface(os.path.join(self.path,self.file_name),self.width,self.height)
        elif self.fmt=='png':
            surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,self.width,self.height)
        ctx=cairo.Context(surface)
        ctx.set_source_rgb(0,0,0)
        ctx.paint()
        self.ctx=ctx
        self.surface=surface

    def genpoint(self,f1,f2,a,b):#x0,y0 is the origin point 
        x = a
        self.data=int((b-a)/self.step)
        points=np.empty((self.data,2),dtype=float)       
        for i in np.arange(0,self.data,step=1,dtype=int):
            points[i,0]=f1(x)*100+self.x0
            points[i,1]=-f2(x)*100+self.y0
            x += self.step
        
        return points
        
        
    def get_buff(self):
        try:
            assert self.fmt=='png'
            return self.surface.get_data()
        except:
            print('only png format file can have buffer data')
            return None
        
        
        
    def get_pixel_array(self):
        return None if self.fmt=='svg' else np.ndarray(shape=(self.width, self.height,4),
                     dtype=np.uint8,
                     buffer=self.get_buff())


    def circle(self,x,y,size=10):
        self.ctx.set_source_rgb(.75,.34,.15)
        self.ctx.arc(*self.d2u_p(x,y),size,0,2*np.pi)    
        self.ctx.fill()
        self.ctx.stroke()
    
    def d2u_r(self,x,y):
        return self.ratio*x,-self.ratio*y
        
    def d2u_p(self,x,y):
        return self.ratio*x+self.x0,-self.ratio*y+self.y0
        
    
    
    def line(self,ctx,x1,y1,x2,y2):
        self.ctx.set_source_rgb(.85,.147,.75)
        self.ctx.move_to(*self.d2u_p(x1,y1))
        self.ctx.line_to(*self.d2u_p(x2,y2))
        self.ctx.set_line_width(3.8)
        self.ctx.stroke()

    def new2old(self,points,a=None,b=None):
        if a is None and b is None:
            a=self.x0
            b=self.y0
        for i in range(self.data):
            points[i,0]+=a
            points[i,1]+=b
        return points

    def old2new(self,points,a=None,b=None):
        if a is None and b is None:
            a=self.x0
            b=self.y0
        for i in range(self.data):
            points[i,0]-=a
            points[i,1]-=b
        return points

    def draw(self,points,grid,axis):       
        self.init_canvas()
        if grid:
            self.setgrid()
        if axis:
            self.setaxis()    
        self.ctx.move_to(*points[0])
        for p in points[1:]:
            self.ctx.line_to(*p)
        self.ctx.set_line_width(5)
        self.ctx.set_source_rgb(*self.rgb)
        self.ctx.stroke()

    def draw_function(self,f1,f2,a,b,*args):
        self.draw(self.genpoint(f1,f2,a,b),*args)
