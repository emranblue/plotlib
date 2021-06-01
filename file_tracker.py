import os,shutil
from plotlib.config import digest_config
from platform import system
class FileManager:
    CONFIG={
        'dirname':None,
        'filename':None,
        'rootpath':os.getcwd(),
        'extent':'_plotlib',
    }

    def __init__(self,dirname=None,filename=None,audiofile=None,**kwargs):
        digest_config(self,kwargs)
        self.dirname=self.name() if not self.dirname else self.dirname
        if filename is not None:
            self.setfilename(filename)
        if dirname:
            self.setdirname(dirname)
        self.path=os.path.join(self.rootpath,self.dirname)
        if not os.path.exists(self.path):
            os.chdir(self.rootpath)
            os.mkdir(self.dirname)
        if self.audiofile:
            self.sendtopath(self.audiofile)
        self.newfile()

    def getfilepath(self):
        return self.path
        
    def sendtopath(self,files):
        shutil.move(files,os.path.join(self.path,files))
        
    def gopath(self):
        os.chdir(self.path)

    def setpath(self,name:str):
        self.path=name

    def getfilename(self)->str:
        return self.filename

    def setfilename(self,name:str):
        self.filename=name  

    def setdirname(self,name:str):
        self.dirname=name


    def getdirname(self)->str:
        return self.dirname
    
    def getextn(self):
        extn=self.filename.split('.')[-1]
        if extn==self.getbase():
            return ".mp4"
        else:
            return '.'+extn
        
    def getbase(self):
        return self.filename.split('.')[0]
        
        
    def name(self):
        return self.__class__.__name__

            
    def newfile(self)->str:
        flist=os.listdir(self.path)
        self.filename=self.getbase()+self.extent+self.getextn()
        if not self.filename in flist:
            return self.filename
        i=0
        while True:
            if self.getbase()+str(i)+self.getextn() in flist:
                i+=1
            else:
                break    
        self.filename=self.getbase()+str(i)+self.getextn()            
        return self.filename


    @classmethod
    def get_name(cls,file_name):
        fmt=file_name.split('.')[-1]
        file_name=file_name.split('.')[0]
        extn='.'+fmt
        flist=os.listdir()
        i=0
        while True:
            if file_name+extn in flist:
                i+=1
            elif file_name+str(i)+extn in flist:
                i+=1
            else:
                break    
        file_name=file_name+str(i)+extn            
        return file_name
	    
    
        

    def show(self):
        os.chdir(self.path)
        assert os.path.exists(self.filename)
        if system()=='Linux':
            os.system('xdg-open {}'.format(self.filename))#only available in linux os
        else:
            print("Go to {}".format(self.path/self.dirname))

       
