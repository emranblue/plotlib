from plotlib.video_writer import VideoWriter
import numpy as np
import sys
if len(sys.argv)>1:
    time=int(sys.argv[1])
else:
    time=120
writer=VideoWriter()
writer.record_screen(time_laps=time,view=True,framerate=112)
