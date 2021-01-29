from parser import get_cli
from function import PerametricFunction,Function,PolarFunction
from util import GraphingTool
import os,sys,numpy
from tqdm import tqdm as ProcessBar
from config import digest_config
from video_writer import VideoWriter
from constant import LOW_QUALITY,MID_QUALITY,HIGH_QUALITY
from rate_func import sigmoid,linear
from file_tracker import FileManager

class Draw(GraphingTool):
    CONFIG={
    'data_file':'plotlib.txt',
    'function':None,
    'lower_limit':'-5',
    'upper_limit':'5',
    'video_file':'plotlib',
    'axis':True,
    'grid':True,
<<<<<<< HEAD
    'run_time':.25,
=======
    'run_time':0.25,
>>>>>>> refs/remotes/origin/main
    'quality':MID_QUALITY,
    'multiplier':6
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
        return sigmoid(numpy.arange(int(self.run_time*self.quality*self.multiplier))/(self.run_time*self.quality))
    

    def view_and_write_data_save_all(self):
        array_data=self.draw(*[True]*3)
        numpy.set_printoptions(threshold=sys.maxsize)
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        ProcessBar(open(self.data_file,'w').write(str(array_data)))
        os.system('vim {}'.format(self.data_file))# vim editor is necessary

	
    def get_combined_func(self,f1:str,f2:str,alpha):
	    return PerametricFunction.homotopy_func(f1,f2,alpha)
	
    def get_movement_pixel_array_at_alpha(self,f1:str,f2:str,alpha):
	    self.set_func(self.get_combined_func(f1,f2,alpha),self.lower_limit,self.upper_limit)
	    return self.draw(array_data=True)
	 
    @staticmethod    
    def get_base_name(fname):
        return fnmae.split('.')[0]
	    
    def get_movement_video(self,f1,f2):
        self.video_file=get_base_name(self.new_video_file_name())
        writer=VideoWriter(get_full_file(self.video_file))
        writer.init_video_file(self.get_movement_pixel_array_at_alpha(f1,f2,self.get_number_of_frame()[0]),self.quality)
        for frame in ProcessBar(self.get_number_of_frame()[1:]):
            writer.start_writing(self.get_movement_pixel_array_at_alpha(f1,f2,frame),self.quality)
        writer.finish_writing()
        writer.viwe_video(get_full_file(self.video_file))
	    
	    


    def delete(self):
        pass


    
