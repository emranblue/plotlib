from grapher import Draw
from tqdm import tqdm as processbar# processing bar showing,silly but effective
run=Draw(mode='video')
run.get_movement_video('x','x**2')
