import numpy as np
from tqdm import tqdm
import os
import ffmpeg
from config import digest_config
class VideoWriter(object):
    CONFIG={
        'video_file':None,
        'video_dir':'video',
        'initial_dir':os.getcwd(),
    }
    def __init__(self,video_file,**kwargs):
        digest_config(self,kwargs)
        self.process=None
        self.video_file=video_file
        if not os.path.exists(self.video_dir):
            os.mkdir(f'{self.video_dir}')
        

    def init_video_file(self, images, framerate, vcodec='libx264'):
        os.chdir(self.video_dir)
        if not isinstance(images, np.ndarray):
            images = np.asarray(images)
        width,height,channels = images.shape
        self.process = (
            ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb32', s='{}x{}'.format(width, height))
                .output(self.video_file, pix_fmt='yuv420p', vcodec=vcodec, r=framerate)
                .overwrite_output()
                .run_async(pipe_stdin=True,quiet=True)
        )


    def start_writing(self,images,framerate):
        self.process.stdin.write(
            images
                .astype(np.uint8)
                .tobytes()
        )

    def finish_writing(self):        
        self.process.stdin.close()
        self.process.wait()
        os.chdir(self.initial_dir)


    def viwe_video(self,file_name):
        os.system(f'xdg-open {file_name}')#only of linux

