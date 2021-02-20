from plotlib.parser import get_cli
from plotlib.function import PerametricFunction,Function,PolarFunction
from plotlib.util import GraphingTool
import os,sys,numpy
from tqdm import tqdm as ProcessBar
from plotlib.config import digest_config
from plotlib.video_writer import VideoWriter
from plotlib.constant import LOW_QUALITY,MID_QUALITY,HIGH_QUALITY
from plotlib.rate_func import sigmoid,linear,homotopy_func,slow_down,return_polar
from plotlib.file_tracker import FileManager

class Draw(GraphingTool):
    CONFIG={
    'data_file':'plotlib.txt',
    'function':None,
    'lower_limit':'-5',
    'upper_limit':'5',
    'video_file':'plotlib',
    'axis':True,
    'grid':True,
    'run_time':2,
    'quality':HIGH_QUALITY,
    }
    def __init__(self,mode='image',**kwargs):
        digest_config(self,kwargs)
        if mode =='image':
            self.args=get_cli()
            if self.args.svg:
                self.fmt='svg'
            else:
                self.fmt='png'
            self.dir_name=self.args.dir_name
            self.file_name=self.args.file_name
            self.upper_limit=self.args.upper_limit
            self.lower_limit=self.args.lower_limit
            if not self.args.rm:
                self.view_and_write_data_save_all()
            else:
                self.delete()
        elif mode=='video':
            self.fmt='png'
            self.vfmt='mp4'
            self.dir_name='plotlib_video'
            self.file_name=self.video_file
            
        elif mode=='point':
            pass
            
    @staticmethod        
    def get_full_file(fname,extn='mp4'):
        return fname+'.'+extn
     
    def set_func(self,func,grid=True,axis=True):
        if hasattr(self,"ars"):
            self.args.plot=True
            self.args.function=PerametricFunction.functionaize(func)    
        else:
            self.function=func

            
    def new_video_file_name(self):
        name=FileManager(self.vfmt,self.dir_name,self.file_name)
        return name.newfile()
        
    def draw(self,func=None,array_data=False,view=False,save=False):
        if hasattr(self,"args"):
            if self.args.plot:
                self.function=Function(self.args.function)
            elif self.args.pera:
                self.function=PerametricFunction(self.args.funtion_x,self.args.function_y)
            elif self.args.polar:
                self.function=PolarFunction(self.args.function)
        else:
            if not func is None:
                self.function=func
        #self.function.setlimit(self.lower_limit,self.upper_limit)
        canvas=GraphingTool(self.fmt,self.dir_name,self.file_name)
        canvas.setlimit(self.lower_limit,self.upper_limit)
        canvas.passfunction(self.function)
        canvas.draw_function(*canvas.getfunction(),*canvas.getlimit(),self.args.grid if hasattr(self,"args") else self.grid,self.args.axis if hasattr(self,"args") else self.axis)
        if save:
            canvas.savefile(canvas.surface)
        if view:
            canvas.view()#optional,used for instant view,not necessary 
        return canvas.get_pixel_array() if array_data else None
        
        
    def get_number_of_frame(self):
        return slow_down(numpy.linspace(0,1,self.run_time*self.quality))
    

    def view_and_write_data_save_all(self):
        array_data=self.draw(*[True]*3)
        numpy.set_printoptions(threshold=sys.maxsize)
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        ProcessBar(open(self.data_file,'w').write(str(array_data)))
        os.system('vim {}'.format(self.data_file))# vim editor is necessary

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
    
	    
    def test_f(self,t):
        return homotopy_func(numpy.array(*[return_polar(lambda x:numpy.exp(numpy.cos(x))-2*numpy.cos(4*x)+numpy.sin(x/4)**3)],dtype=object),numpy.array([lambda x:3*numpy.cos(x),lambda x:3*numpy.sin(x)],dtype=object),t)
        
        
        
    def test_method(self):
        self.video_file=Draw.get_base_name(self.new_video_file_name())
        writer=VideoWriter(Draw.get_full_file(self.video_file))
        writer.play_interpolate(self.test_f,self.get_number_of_frame(),-5,5,self.quality)
        writer.view_video(Draw.get_full_file(self.video_file)) 
        
        
        
    def test_3D(self,points):
        canvas=GraphingTool(self.fmt,self.dir_name,self.file_name)
        canvas.join_3D_points(points)
        canvas.savefile(canvas.surface)
        canvas.view()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def get_combined_func(self,f1:str,f2:str,alpha):
        return PerametricFunction.homotopy_func(f1,f2,alpha)
	    
	    
    def get_movement_pixel_array_at_alpha(self,f1:str,f2:str,alpha):
	    self.set_func(self.get_combined_func(f1,f2,alpha),self.lower_limit,self.upper_limit)
	    return self.draw(array_data=True)
	    
    
	 
    @staticmethod    
    def get_base_name(fname):
        return fname.split('.')[0]
	    
    def get_movement_video(self,f1,f2):
        self.video_file=Draw.get_base_name(self.new_video_file_name())
        writer=VideoWriter(Draw.get_full_file(self.video_file))
        writer.init_video_file(self.get_movement_pixel_array_at_alpha(f1,f2,self.get_number_of_frame()[0]),self.quality)
        for frame in ProcessBar(self.get_number_of_frame()[1:]):
            writer.start_writing(self.get_movement_pixel_array_at_alpha(f1,f2,frame),self.quality)
        writer.finish_writing()
        writer.viwe_video(Draw.get_full_file(self.video_file))
	    
	    


    def delete(self):
        pass


    
