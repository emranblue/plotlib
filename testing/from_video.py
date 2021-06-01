from ffmpeg import FFMPEG_VideoWriter
import cv2,os,shutil
from subprocess import getoutput
from tqdm import tqdm
from file_tracker import FileManager
from image import setalpha
from config import digest_config
class FromVideo(FFMPEG_VideoWriter,FileManager):
    CONFIG={
    'fps':None,
    'initiate':True,
    'file_writing':True,
    'capture':True,
    
    }
    ##kind of base class for other stuff from video
    def __init__(self,filename=None,source=None,allow_audio=False,view=False,**kwargs):
        digest_config(self,kwargs)
        FFMPEG_VideoWriter.__init__(self,**kwargs)
        FileManager.__init__(self,filename=filename)
        if self.capture:
            self.allow_audio=allow_audio
            self.view=view
            self.cap=cv2.VideoCapture(filename if source is None else source)
            self.setfps(self.getfps()) if self.fps is None else self.fps
            if self.file_writing:
                print("\n\nWriting to file: "+self.filename)
            self.setsize(self.getpixel())
            self.setfilename(self.filename)
            if allow_audio and self.audiofile is None:
                self.setaudio(self.getaudiofromfile(filename))
        
            if self.initiate:
                self.init()



    def getnframes(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_COUNT) if self.capture else None

    def getfps(self):
        return self.cap.get(cv2.CAP_PROP_FPS) if self.capture else None
         
    def getaudiofromfile(self,filename,exten=".mp3"):
       audio=filename.split('.')[0]+exten
       getoutput("ffmpeg -y -i {} {}".format(filename,audio))
       self.sendtopath(audio)
       return audio
       
    def init(self):
        self.print_info()
        self.gopath()
        self.init_video()
        

    def read(self):
        return self.cap.read()

    def print_info(self):
        print('\n\nVideo framerate: ',self.getfps())
        print('Number of Frame: ',self.getnframes())
        print("\nWriting to FFMPEG buffer...\n")

    def getpixel(self):
        status,pixel_array= self.read()
        assert status
        return pixel_array

    def isOpened(self):
        return self.cap.isOpened()

    def print_end(self):
        print("\nFinish Writing.")
        if self.audiofile:
            shutil.move(self.audiofile,os.path.join(self.rootpath,self.audiofile))

class ApplyMethodToVideo(FromVideo):
    
    ##any method that modify pixel array
    CONFIG={
    'method':None,
    }

    def __init__(self,method=None,**kwargs):
        #self.method=method if callable(method) else None
        FromVideo.__init__(self,**kwargs)
        if callable(method):
            self.method=method
    def make(self,**kwargs):
        '''All the perameter for the given method is valid only the first perameter pixel_array must not provide to this fucntion ,rest of them is ok'''    
        
        assert self.method is not None
        self.processbar=tqdm(total=self.getnframes())
        self.processbar.update(1)
        while self.isOpened():
            status,pixel_array=self.read()
            if status:
                pixel_array=setalpha(pixel_array)
                pixel_array=self.method(pixel_array,**kwargs)
                self.write_frame(pixel_array)
                self.processbar.update(1)
            else:
                break
        self.cap.release()
        self.close()
        self.processbar.close()
        self.print_end()
        if self.view:
            self.show()

        
        
class Meme(ApplyMethodToVideo):
    from meme import meme2array
    CONFIG={
    'method':meme2array,
    'allow_audio':True,
    }



class Combine(ApplyMethodToVideo):
    CONFIG={
    'method':lambda m:m,
    'rgb':False
    }
    
    def __init__(self,filename,audiofile,**kwargs):
        ApplyMethodToVideo.__init__(self,filename=filename,audiofile=audiofile,**kwargs)
        FileManager.__init__(self,filename=filename,audiofile=audiofile,**kwargs)
        self.make()
        
        
class GetVideo(ApplyMethodToVideo):
    CONFIG={
    'method':lambda m:m,
    'rgb':False,
    'allow_audio':False
    }
    def __init__(self,filename,**kwargs):
        ApplyMethodToVideo.__init__(self,filename=filename,**kwargs)
        self.make()
        
    
    
    
class GetAudio(FromVideo):
    CONFIG={
    'capture':False,
    'extent':'',
    }
    
    def __init__(self,filename,**kwargs):
        FromVideo.__init__(self,filename=filename,**kwargs)
        self.getaudiofromfile(self.filename)


