from parser import get_cli
from function import PerametricFunction,Function,PolarFunction
from util import GraphingTool
import os,sys,numpy
from tqdm import tqdm as ProcessBar
from config import digest_config
from video_writer import VideoWriter
from constant import LOW_QUALITY,MID_QUALITY,HIGH_QUALITY
from rate_func import sigmoid,linear

class Draw(GraphingTool):
    CONFIG={
    'data_file':'test.txt',
    'function':None,
    'lower_limit':'-5',
    'upper_limit':'5',
    'video_file':'test.mp4',
    'axis':True,
    'grid':True,
    'run_time':5,
    'quality':HIGH_QUALITY,
    'data_file':'test.txt',
    'multiplier':3
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
            self.dir_name='video_dir'
            self.file_name='temp'
     
    def set_func(self,func,grid=True,axis=True):
        if hasattr(self,"ars"):
            self.args.plot=True
            self.args.function=PerametricFunction.functionaize(func)    
            #self.args.lower_limit,self.upper_limit=lower_limit,upper_limit
        else:
            self.function=func

            
        
    def draw(self,func=None,array_data=False,view=False,save=False):
        '''if hasattr(self,"args"):
            if self.args.plot:
                function=Function(self.args.function)
            elif self.args.pera:
                function=PerametricFunction(self.args.funtion_x,self.args.function_y)
            elif self.args.polar:
                function=PolarFunction(self.args.function)
        else:
            if not func:
                function=self.function
                #function.setlimit(self.lower_limit,self.upper_limit)
            else:
                function=func'''
        #function.setlimit(self.lower_limit,self.upper_limit)
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
        return sigmoid(numpy.arange(self.run_time*self.quality*self.multiplier)/(self.run_time*self.quality))
    

    def view_and_write_data_save_all(self):
        array_data=self.draw(*[True]*3)
        numpy.set_printoptions(threshold=sys.maxsize)
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        ProcessBar(open(self.data_file,'w').write(str(array_data)))
        os.system(f'vim {self.data_file}')# vim editor is necessary

	
    def get_combined_func(self,f1:str,f2:str,alpha):
	    return PerametricFunction.homotopy_func(f1,f2,alpha)
	
    def get_movement_pixel_array_at_alpha(self,f1:str,f2:str,alpha):
	    self.set_func(self.get_combined_func(f1,f2,alpha),self.lower_limit,self.upper_limit)
	    return self.draw(array_data=True)
	    
    def get_movement_video(self,f1,f2):
        writer=VideoWriter(self.video_file)
        writer.init_video_file(self.get_movement_pixel_array_at_alpha(f1,f2,self.get_number_of_frame()[0]),self.quality)
        for frame in ProcessBar(self.get_number_of_frame()[1:]):
            writer.start_writing(self.get_movement_pixel_array_at_alpha(f1,f2,frame),self.quality)
        writer.finish_writing()
        writer.viwe_video(self.video_file)
	    
	    


    def delete(self):
        pass


    
