from ffmpeg import FFMPEG_VideoWriter
from config import digest_config
from image import cairo2array
import datetime,time,os
import numpy as np
import pyautogui
from tqdm import tqdm
class ScreenRecord(FFMPEG_VideoWriter):
    CONFIG={
            'filename':str(datetime.datetime.now())+'.mp4',
            'fps':10,
            'rgb':True,
            'wait':3,
            }
    def __init__(self,filename=None,box=None,custom_box=False,**kwargs):
        digest_config(self,kwargs)
        FFMPEG_VideoWriter.__init__(self,filename=self.filename,fps=self.fps,rgb=self.rgb,**kwargs)
        if box is None and custom_box:
            box=self.getbox()
        self.setsize(self.getsize(box))
        self.init_video()
        self.getting_ready()
        self.record(box)

    def getsize(self,box):
        return self.grabscreen(box)
        
        
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
        return x0,y0,x1,y1
        
    def counter(self):
        for i in range(self.wait,0,-1):
            os.system('clear')
            print(i)
            time.sleep(1)
        os.system('clear')
        
        
    def getting_ready(self):
        print("Preparing...")
        time.sleep(self.wait)
        
        
        
    def y_position(self):
        return self.getposition()[1]

    def grabscreen(self,box):
        img = pyautogui.screenshot(region=box)
        img.putalpha(255)
        frame = np.array(img).astype(np.uint8)
        return frame
    
    def record(self,box):
        bar=tqdm()
        try:
            bar.update(1)
            while True:
                self.write_frame(self.grabscreen(box))
                bar.update(1)
        except KeyboardInterrupt:
            self.close()
            bar.close()





