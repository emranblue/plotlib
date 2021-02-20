import numpy as np
import ffmpeg,os,time,cairo,subprocess
from config import digest_config
from util import GraphingTool
from tqdm import tqdm as ProcessBar
from rate_func import map_func_array,cairo_context_to_pixel_array
from multiprocessing import Process
from contextlib import redirect_stdout as stout
from image import array2cairo,cairo2array,init_cairo_surface,cairo_create,invert
from pyautogui import screenshot
from meme import meme2array
import cv2
from platform import system
from PIL import Image
from file_tracker import FileManager
class VideoWriter(object):
    #class perpose for writing raw image data to ffmpeg buffer
    CONFIG={
        'video_file':'plotlib.mp4',
        'video_dir':'plotlib_video',
        'initial_dir':os.getcwd(),
        'vcodec':'libx264',
        'audio_file':'temp.mp3',
        'pixel_format':'rgb32',
    }
    
    

    
    def __init__(self,video_file=None,**kwargs):
        digest_config(self,kwargs)
        self.process=None
        if video_file:
            self.video_file=video_file
        
        
    def rename(self):
        self.video_file=FileManager.get_name(self.video_file)
            
            
            
    def make_video_dir(self):
        if not os.path.exists(self.video_dir):
            os.mkdir('{}'.format(self.video_dir))
        
        
    #take numpy array as input then write that array to ffmpeg buffer,
    
    
    def init_video_file(self, pixel_array, framerate, width=None, height=None,vcodec=None,pixel_format=None):
        self.make_video_dir()
        os.chdir(self.video_dir)
        self.rename()
        if vcodec:
            self.vcodec=vcodec
        if not isinstance(pixel_array, np.ndarray):
            pixel_array = np.asarray(pixel_array)
        if not width:
            width,height,_= pixel_array.shape
        self.process = (
            ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt=self.pixel_format, s='{}x{}'.format(width, height))
                .output(self.video_file, pix_fmt='yuv420p', vcodec=self.vcodec, r=framerate)
                .overwrite_output()
                .run_async(pipe_stdin=True,quiet=True)
        )
        

    #this method will lie on a  loop and continously writing array to buffer for creating video 
    
    
    def start_writing(self,pixel_array,invert_=False):
        if invert_:
            pixel_array=invert(pixel_array)
        self.process.stdin.write(
            pixel_array
                .astype(np.uint8)
                .tobytes()
        )


    def finish_writing(self,view=True):        
        self.process.stdin.close()
        self.process.wait()
        if view:
            self.view_video()
    
    
        
        
    def play_interpolate(self,generating_func,alpha_array,a,b,framerate,grid=True,axis=True,vcodec=None):
        func_data=GraphingTool()
        self.init_video_file(func_data.func_to_buffer(*generating_func(alpha_array[0]),a,b,grid,axis),framerate)
        for f_x,f_y in ProcessBar(map_func_array(generating_func,alpha_array)):
            self.start_writing(func_data.func_to_buffer(f_x,f_y,a,b,grid,axis))
        self.finish_writing()
        
        
    
    def grab_screen_PIL(self,box):
        img = screenshot(region=box)
        img.putalpha(255)
        frame = np.array(img).astype(np.uint8)
        return frame
        
    def grab_screen_GDK(self,box):
        from gi.repository import Gdk
        window=Gdk.get_default_root_window()
        if not box:
            x0,y0,width,height=window.get_geometry()
        else:
            x0,y0,width,height=box
        surface
        data=window.cairo_create().get_target()
        return cairo2array(data) 
        
    
    def running(self,starting_time,time_laps):
        if self.now()-starting_time<time_laps:
            return True
        else:
            return False 
        
        
        
    def now(self):
        return int(time.time())
    
    
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


    def init_timer(self,wait):
        for i in range(wait,0,-1):
            os.system('clear')
            print(i)
            time.sleep(1)
        os.system('clear')


    def record_screen(self,time_laps,box=None,framerate=9,audio=False,wait=5,view=False,tool='pil',invert=False):
        self.init_timer(wait)
        if tool=='pil':
            self.grab_screen=self.grab_screen_PIL
        else:
            self.grab_screen=self.grab_screen_GDK
        pix_array=self.grab_screen(box)
        self.init_video_file(pix_array,framerate,width=pix_array.shape[1], height=pix_array.shape[0])
        if audio:
            with stout(None):
                self.audio_process()
        processbar=ProcessBar()
        start=self.now()
        while self.running(start,time_laps):
            self.start_writing(self.grab_screen(box),invert)
            #time.sleep(1/framerate)  #as python is slow ,no ne
            processbar.update(1)
        self.finish_writing()
        processbar.close()
        if audio:
            self.terminate_audio()
            



    def view_video(self):
        if system()=='Linux':
            os.system('xdg-open {}'.format(self.video_file))#only of linux
        os.chdir(self.initial_dir)


    def get_meme_name(self,name):
        return name.split('.')[0]+'_meme.'+name.split('.')[1]


    def meme(self,video_file,caption='',width=80,color=[1,1,1,1],direction='down',border=30,font="Courier New",font_size=36,view=True,invert=False):
    
        self.video_file=self.get_meme_name(video_file)
        cap=cv2.VideoCapture(str(video_file))
        fps=int(cap.get(cv2.CAP_PROP_FPS))
        frame_num=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print('Video framerate: ',fps)
        print('Number of Frame: ',frame_num)
        print("\nWriting to FFMPEG buffer...\n")
        status,pixel_array=cap.read()
        im=Image.fromarray(pixel_array)
        im.putalpha(256)
        pixel_array=np.array(im)
        processbar=ProcessBar(total=frame_num)
        self.init_video_file(pixel_array,fps,width=pixel_array.shape[1],height=pixel_array.shape[0])
        self.start_writing(meme2array(pixel_array,caption,width,color,direction,border,font,font_size),invert)
        processbar.update(1)
        while cap.isOpened():
            status,pixel_array=cap.read()
            if status:
                im=Image.fromarray(pixel_array)
                im.putalpha(256)
                pixel_array=np.array(im)
                modified_pixel_array=meme2array(pixel_array,caption,width,color,direction,border,font,font_size)
                self.start_writing(modified_pixel_array,invert)
                processbar.update(1)
            else:
                break
        self.finish_writing(view)
        processbar.close()
        print("\nFinish Writing.")
        



