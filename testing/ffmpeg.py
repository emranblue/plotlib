
import os,sys
import subprocess as sp

import numpy as np

from tqdm import tqdm as ProcessBar
import cv2
from image import invert,setalpha
from meme import meme2array


class FFMPEG_VideoWriter:


    def __init__(self, filename=None, size=None, fps=None, codec="libx264", audiofile=None,
                 preset="medium", bitrate=None, withmask=False,
                 logfile=None, threads=None, ffmpeg_params=None,invert=False,rgb=False):

        if logfile is None:
            logfile = sp.PIPE

        self.filename = filename
        self.size=size
        self.rgb=rgb
        self.codec = codec
        self.fps=fps
        self.preset=preset
        self.bitrate=bitrate
        self.withmask=withmask
        self.threads=threads
        self.logfile=logfile
        self.ffmpeg_params=ffmpeg_params
        self.audiofile=audiofile
        self.invert=invert
        self.ext=self.filename.split('.')[-1] if filename is not None else "mp4"

    
    def setaudio(self,audiofile):
        self.audiofile=audiofile
        
    def setcodec(self,codec):
        self.codec=codec
        
    def setpreset(self,preset):
        self.preset=preset
    
    def setfilename(self,filename):
        self.filename=filename 
       
    def setfps(self,fps):
        self.fps=fps
       
        
    def setinvert(self):
        self.invert=True
    
    def setsize(self,pixel_array):
        width,height,_= pixel_array.shape
        if width<height:
            width,height=height,width
        self.size=(width,height)
        
    def init_video(self):
    
        cmd = [
            'ffmpeg',
            '-y',
            '-loglevel', 'error' if self.logfile == sp.PIPE else 'info',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', '%dx%d' % (self.size[0], self.size[1]),
            '-pix_fmt', 'rgba' if self.rgb else 'bgra'  ,
            '-r', '%.02f' % self.fps,
            '-an', '-i', '-'
        ]
        if self.audiofile is not None:
            cmd.extend([
                '-i', self.audiofile,
                '-acodec', 'copy'
            ])
        cmd.extend([
            '-vcodec', self.codec,
            '-preset', self.preset,
        ])
        if self.ffmpeg_params is not None:
            cmd.extend(self.ffmpeg_params)
        if self.bitrate is not None:
            cmd.extend([
                '-b', self.bitrate
            ])

        if self.threads is not None:
            cmd.extend(["-threads", str(self.threads)])

        if ((self.codec == 'libx264') and
                (self.size[0] % 2 == 0) and
                (self.size[1] % 2 == 0)):
            cmd.extend([
                '-pix_fmt', 'yuv420p'
            ])
        cmd.extend([
            self.filename
        ])

        popen_params = {"stdout": sp.DEVNULL,
                        "stderr": self.logfile,
                        "stdin": sp.PIPE}
        if os.name == "nt":
            popen_params["creationflags"] = 0x08000000 

        self.proc = sp.Popen(cmd, **popen_params)


    def write_frame(self, img_array):
    
        if self.invert:
            img_array=invert(img_array)
        self.proc.stdin.write(img_array.tobytes())
        
        
        
    def close(self):
    
        if self.proc:
            self.proc.stdin.close()
            if self.proc.stderr is not None:
                self.proc.stderr.close()
            self.proc.wait()

        self.proc = None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

