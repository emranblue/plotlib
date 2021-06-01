from plotlib.ffmpeg import FFMPEG_VideoWriter
from plotlib.config import digest_config
from plotlib.image import cairo2array
import datetime,time,os,mss,tkinter
import numpy as np
import pyautogui
from tqdm import tqdm
class ScreenRecord(FFMPEG_VideoWriter):
    CONFIG={
            'filename':str(datetime.datetime.now())+'.mp4',
            'fps':18,
            'rgb':False,
            'wait':3,
            }
    def __init__(self,filename=None,box=None,custom_box=False,view=False,**kwargs):
        digest_config(self,kwargs)
        self.view=view
        FFMPEG_VideoWriter.__init__(self,filename=self.filename,fps=self.fps,rgb=self.rgb,**kwargs)
        if box is None and custom_box:
            box=self.getbox()
        elif box:
            box=self.dictify(box)
        self.screen=mss.mss()
        self.monitor=box
        if not self.monitor:
            self.set_window()
        self.setsize(self.getsize())
        self.init_video()
        self.getting_ready()
        self.record()
        self.display()
        
        
    def display(self):
        if self.view:
            os.system("xdg-open '{}'".format(self.filename))

    def getsize(self):
        return self.grabscreen()
        
        
    def getposition(self):
        return pyautogui.position()
        
    def x_position(self):
        return self.getposition()[0]
        
        
    def getbox(self):
        self.counter()
        print("left corner")
        time.sleep(1)
        x0,y0=self.getposition()
        self.counter()
        print("right corner")
        x1,y1=self.getposition()
        return self.dictify((x0,y0,x1,y1))
        
    @staticmethod    
    def dictify(args):
        return {'top':args[0],'left':args[1],'width':args[2]-args[0],'height':args[3]-args[1]}
    
        
    def counter(self):
        for i in range(self.wait,0,-1):
            os.system('clear')
            print(i)
            time.sleep(1)
        os.system('clear')
        
        
    def getting_ready(self):
        print("Preparing...")
        time.sleep(self.wait)
        
    def set_window(self):
        root = tkinter.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        self.monitor={'top':0,'left':0,'width':width,'height':height}
        
        
    def y_position(self):
        return self.getposition()[1]
        
    def grabscreen(self):
        frame=np.array(self.screen.grab(self.monitor))
        return frame
    
    
    def record(self):
        bar=tqdm()
        try:
            bar.update(1)
            while True:
                self.write_frame(self.grabscreen())
                time.sleep((1/self.fps)-0.01)
                bar.update(1)
        except KeyboardInterrupt:
            self.close()
            bar.close()





