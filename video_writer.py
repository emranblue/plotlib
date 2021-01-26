import numpy as np
from tqdm import tqdm
import ffmpeg
from config import digest_config
class VideoWriter(object):
    CONFIG={
        'video_file':None
    }
    def __init__(self,video_file,**kwargs):
        digest_config(self,kwargs)
        self.process=None
        self.video_file=video_file

    def init_video_file(self, images, framerate, vcodec='libx264'):
        if not isinstance(images, np.ndarray):
            images = np.asarray(images)
        n,height,width,channels = images.shape
        self.process = (
            ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
                .output(self.video_file, pix_fmt='yuv420p', vcodec=vcodec, r=framerate)
                .overwrite_output()
                .run_async(pipe_stdin=True)
        )


    def start_writing(self,images,framerate):
        self.init_video_file(images,framerate)
        #for frame in tqdm(images):
        self.process.stdin.write(
            images
                .astype(np.uint8)
                .tobytes()
        )

    def finish_writing(self):        
        self.process.stdin.close()
        self.process.wait()

