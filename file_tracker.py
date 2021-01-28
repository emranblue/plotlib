import os
from config import digest_config
from platform import system
class FileManager:
    CONFIG={
        "fmt":'png',
        'dir_name':'image',
        'file_name':'plotlib_img',
    }

    def __init__(self,fmt,dir_name,file_name,**kwargs):
        digest_config(self,kwargs)
        if fmt:
            self.setfmt(fmt)
        if file_name:
            self.setfilename(file_name)
        if dir_name:
            self.setdirname(dir_name)
        path=os.path.join(os.getcwd(),self.dir_name)
        if not os.path.exists(path):
            os.mkdir(self.dir_name)
        self.setpath(path)

    def getfilepath(self):
        return self.path

    def setpath(self,name:str):
        self.path=name

    def getfilename(self)->str:
        return self.file_name

    def setfilename(self,name:str):
        self.file_name=name  

    def setdirname(self,name:str):
        self.dir_name=name

    def setfmt(self,name:str):
        self.fmt=name

    def getdirname(self)->str:
        return self.dir_name

            
    def newfile(self)->str:
        extn='.'+self.fmt
        flist=os.listdir(self.path)
        i=0
        while True:
            if self.file_name+str(i)+extn in flist:
                i+=1
            else:
                break    
        self.file_name=self.file_name+str(i)+extn            
        return self.file_name


    def savefile(self,surface):
        if self.fmt=='png':
            surface.write_to_png(os.path.join(self.path,self.newfile()))
        elif self.fmt=='svg':
            surface.finish()
    
        

    def view(self):
        os.chdir(self.path)
        assert os.path.exists(self.file_name)
        if system()=='Linux':
            os.system('xdg-open {}'.format(self.file_name))#only available in linux os
        else:
            print("Go to {}".format(self.path/self.dir_name))


    def removefile(self,name):
        os.chdir(self.path)
        if len(os.listdir()):
            if name.isdigit():
                os.remove(self.file_name+name+'.'+self.fmt)
            elif name=='all' or name=="*":
                os.system('rm *.{}'.format(self.fmt))
            print('deleted')
        else:
            print('empty folder') 


    def listdir(self):
        os.chdir(self.path)
        os.system('ls')         
