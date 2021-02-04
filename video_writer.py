import numpy as np
import ffmpeg,os
from config import digest_config
from util import GraphingTool
from tqdm import tqdm as ProcessBar
from rate_func import map_func_array
class VideoWriter(object):
    #class perpose for writing raw image data to ffmpeg buffer
    CONFIG={
        'video_file':'temp',
        'video_dir':'plotlib_video',
        'initial_dir':os.getcwd(),
        'vcodec':'libx264'
    }
    
    
    def __init__(self,video_file,**kwargs):
        digest_config(self,kwargs)
        self.process=None
        self.video_file=video_file
            
            
    def make_video_dir(self):
        if not os.path.exists(self.video_dir):
            os.mkdir('{}'.format(self.video_dir))
        
        
    #take numpy array as input then write that array to ffmpeg buffer,
    
    
    def init_video_file(self, pixel_array, framerate, vcodec=None):
        os.chdir(self.video_dir)
        self.make_video_dir()
        if vcodec:
            self.vcodec=vcodec
        if not isinstance(pixel_array, np.ndarray):
            pixel_array = np.asarray(pixel_array)
        width,height,_= pixel_array.shape
        self.process = (
            ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb32', s='{}x{}'.format(width, height))
                .output(self.video_file, pix_fmt='yuv420p', vcodec=self.vcodec, r=framerate)
                .overwrite_output()
                .run_async(pipe_stdin=True,quiet=True)
        )
        

    #this method will lie on a  loop and continously writing array to buffer for creating video 
    
    
    def start_writing(self,pixel_array,framerate):
        self.process.stdin.write(
            pixel_array
                .astype(np.uint8)
                .tobytes()
        )


    def finish_writing(self):        
        self.process.stdin.close()
        self.process.wait()
    
    
    def iteratively_writing_frame(self,pixel_array:np.ndarray, number_of_frame:int, framerate:int, vcodec=None):
        self.init_video_file(self,pixel_array, framerate, vcodec)
        for frame in ProcessBar(np.arange(number_of_frame)):
            self.start_writing(pixel_array,framerate)
        self.finish_writing()
        
        
        
        
    def play_interpolate(self,generating_func,alpha_array,a,b,framerate,grid=True,axis=True,vcodec=None):
        func_data=GraphingTool()
        self.init_video_file(func_data.func_to_buffer(*generating_func(alpha_array[0]),a,b,grid,axis),framerate)
        for f_x,f_y in ProcessBar(map_func_array(generating_func,alpha_array)):
            self.start_writing(func_data.func_to_buffer(f_x,f_y,a,b,grid,axis),framerate)
        self.finish_writing()
        
        

    def view_video(self,file_name):
        os.system('xdg-open {}'.format(file_name))#only of linux
        os.chdir(self.initial_dir)



