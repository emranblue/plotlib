from plotlib.video_writer import VideoWriter
from plotlib.imageobj import interpolate_between_image,buffer_of_image
import numpy as np
writer=VideoWriter()
writer.record_screen(5)
writer.view_video('temp.mp4')
