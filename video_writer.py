import numpy as np
import ffmpeg,os,time,cairo,subprocess
from plotlib.config import digest_config
from plotlib.util import GraphingTool
from tqdm import tqdm as ProcessBar
from plotlib.rate_func import map_func_array,cairo_context_to_pixel_array
from multiprocessing import Process
from contextlib import redirect_stdout as stout
from gi.repository import Gdk
from plotlib.image import array2cairo,cairo2array,init_cairo_surface

class VideoWriter(object):
    #class perpose for writing raw image data to ffmpeg buffer
    CONFIG={
        'video_file':'temp.mp4',
        'video_dir':'plotlib_video',
        'initial_dir':os.getcwd(),
        'vcodec':'libx264',
        'audio_file':'temp.mp3',
    }
    
    

    
    def __init__(self,video_file=None,**kwargs):
        digest_config(self,kwargs)
        self.process=None
        if not video_file:
            self.video_file=video_file
            
            
    def make_video_dir(self):
        if not os.path.exists(self.video_dir):
            os.mkdir('{}'.format(self.video_dir))
        
        
    #take numpy array as input then write that array to ffmpeg buffer,
    
    
    def init_video_file(self, pixel_array, framerate, vcodec=None):
        self.make_video_dir()
        os.chdir(self.video_dir)
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
    
    
    def start_writing(self,pixel_array):
        self.process.stdin.write(
            pixel_array
                .astype(np.uint8)
                .tobytes()
        )


    def finish_writing(self):        
        self.process.stdin.close()
        self.process.wait()
    
    
        
        
    def play_interpolate(self,generating_func,alpha_array,a,b,framerate,grid=True,axis=True,vcodec=None):
        func_data=GraphingTool()
        self.init_video_file(func_data.func_to_buffer(*generating_func(alpha_array[0]),a,b,grid,axis),framerate)
        for f_x,f_y in ProcessBar(map_func_array(generating_func,alpha_array)):
            self.start_writing(func_data.func_to_buffer(f_x,f_y,a,b,grid,axis))
        self.finish_writing()
        
        
    
    def grab_screen(self,box):
        window=Gdk.get_default_root_window()
        if not box:
            x0,y0,width,height=window.get_geometry()           
        else:
            x0,y0,width,height=box
            
        surface=init_cairo_surface(width-x0,height-y0)
        ctx=cairo.Context(surface)
        ctx.set_source_surface(window.cairo_create().get_target())
        ctx.paint()
        return cairo2array(surface)
          
    def audio_process(self):
        
        self.audio_process=subprocess.Popen(["sox",
        "-t",
        "pulseaudio",
        "alsa_output.pci-0000_00_1b.0.analog-stereo.monitor",
        "-t",
        "mp3",
        "temp.mp3"],
        stdout=subprocess.DEVNULL,
        shell=True)


    def terminate_audio(self):
        self.audio_process.kill()



    def record_screen(self,time_laps,box=None,framerate=30,audio=False):
        pix_array=self.grab_screen(box)
        self.init_video_file(pix_array,framerate)
        if audio:
            with stout(None):
                self.audio_process()
        for frame in ProcessBar(np.arange(framerate*time_laps)):
            self.start_writing(self.grab_screen(box))
            time.sleep(1/framerate)
        self.finish_writing()
        if audio:
            self.terminate_audio()
            



    def view_video(self,file_name):
        os.system('xdg-open {}'.format(file_name))#only of linux
        os.chdir(self.initial_dir)



