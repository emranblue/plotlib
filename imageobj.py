import cairo,os,sys
import numpy as np

def buffer_of_image(image:str):
    im=cairo.ImageSurface.create_from_png(image)
    return np.ndarray(shape=(im.get_width(),im.get_height(),4),
            dtype=np.uint8,
            buffer=im.get_data())


def get_text_name(fname:str):
    return fname.split('.')[0]+'.txt'



def display_png_data(image:str):
    pixel_array=buffer_of_image(image)
    file_name=get_text_name(image)
    np.set_printoptions(threshold=sys.maxsize)
    with open('{}'.format(file_name),'w') as fl:
        fl.write(str(pixel_array))
    os.system('xdg-open {}'.format(file_name))
    
if __name__=='__main__':
    display_png_data(sys.argv[1])
