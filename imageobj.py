import cairo,os,sys
import numpy as np
    
def cairo2array(surface):
    return cairo_context_to_pixel_array(surface)
    
def image2cairo(image):
    return cairo.ImageSurface.create_from_png(image)
    
def cairo2image(surface):
    array2image(cairo2array(surface))
    
def array2cairo(pixel_array):
    return cairo.ImageSurface.create_for_data(pixel_array,cairo.FORMAT_ARGB32,*[inf for inf in pixel_array.shape[0:2]])
    
def image2array(image,full=False):
    if full:
        np.set_printoptions(threshold=sys.maxsize)
    return buffer_of_image(image)

def array2image(pixel_array,file_name='using_imgobj'):
    view_from_array(pixel_array,file_name)

def image2text(image,file_write=True):
    display_png_data(image)

def invert2image(image):
    array2image(invert(image))


def invert(image):
    if isinstance(image,str):
        pixel_array=image2array(image)
    elif isinstance(image,np.ndarray):
        pixel_array=image
    return np.array([255,255,255,2*255]-pixel_array,dtype=np.uint8)
        


def cairo_context_to_pixel_array(surface):
    return np.ndarray(shape=(surface.get_width(),surface.get_height(),4),dtype=np.uint8,buffer=surface.get_data())

    
def view_from_array(pixel_array,file_name):
    surface=array2cairo(pixel_array)
    surface.write_to_png('{}.png'.format(file_name))
    os.system('xdg-open {}.png'.format(file_name))

    
def interpolate_between_image(image1,image2,alpha):
    return np.mod((1-alpha)*buffer_of_image(image1)+alpha*buffer_of_image(image2),256)


def get_text_name(fname:str):
    return fname.split('.')[0]+'.txt'


def display_png_data(image,file_write=False):
    if isinstance(image,str):
        pixel_array=buffer_of_image(image)
        file_name=get_text_name(image)
    elif isinstance(image,np.ndarray):
        pixel_array=image
        file_name="pixel_array"
    np.set_printoptions(threshold=sys.maxsize)
    if file_write:
        with open('{}'.format(file_name),'w') as fl:
            fl.write(str(pixel_array))
        os.system('xdg-open {}'.format(file_name))
    else:
        print(pixel_array)

def buffer_of_image(image):
    return cairo_context_to_pixel_array(image2cairo(image))   

    
if __name__=='__main__':
    display_png_data(sys.argv[1])
    
    
    
