import cairo,os,sys
import numpy as np
from platform import system

def init_cairo_surface(width,height):
    return cairo.ImageSurface(cairo.FORMAT_ARGB32,width,height)
    
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


def mul2image(image,n):
    array2image((n*image2array(image)%256).astype(np.uint8))

def add2image(image,n,alpha):
    array2image((image2array(image)+[n,n,n,alpha]).astype(np.uint8))

def add_vec2image(image,vector,alpha=0):
    if len(vector)==3:
        alpha=255
    array2image((image2array(image)+[*vector,alpha]).astype(np.uint8))
    
def apply_mat2array(image,matrix):
    assert len(matrix)==4
    matrix=np.array(matrix)
    pixel_array=image2array(image)
    width,height=pixel_array.shape[0:2]
    for i in np.arange(width):
        for j in np.arange(height):
            pixel_array[i,j]=(np.matmul(matrix,pixel_array[i,j])%256).astype(np.uint8) 
    return pixel_array  
    
def apply_matrix2image(image,matrix,x0=0,y0=0):
    pixel_array=image2array(image)
    surface=init_cairo_surface(*pixel_array.shape[0:2])
    matrix=cairo.Matrix(*matrix,x0,y0)
    ctx=cairo.Context(surface)
    ctx.set_matrix(matrix)
    ctx.set_source_surface(array2cairo(pixel_array))
    pixel_array=cairo2array(surface)
    array2image(pixel_array)
    
    
    
def apply_mat2image(image,matrix):
    array2image(apply_mat2array(image,matrix))

def invert(image):
    if isinstance(image,str):
        pixel_array=image2array(image)
    elif isinstance(image,np.ndarray):
        pixel_array=image
    return np.array([255,255,255,2*255]-pixel_array,dtype=np.uint8)


def set_pixel(image,target,pixel):
    pixel_array=image2array(image)
    pixel_array[target[0],target[1]]=pixel
    return pixel_array
    
    

def modify_pixel(pixel_array,color,x0,y0,x,y,direction):
    if direction=='down':
        y0,y=y,y0
    surface=array2cairo(pixel_array)
    ctx=cairo.Context(surface)
    ctx.rectangle(x0,y0,x,y)
    ctx.set_source_rgba(*color)
    ctx.fill()
    return cairo2array(surface)
      

def meme_template(image,width=80,color=[255,255,255,255],direction='up'):
    pixel_array=image2array(image)
    color=np.array(color)/255
    if direction =='up':
        array2image(modify_pixel(pixel_array,color,0,0,pixel_array.shape[0],width,direction))
    elif direction=='down':
        array2image(modify_pixel(pixel_array,color,0,pixel_array.shape[1],pixel_array.shape[0],pixel_array.shape[1]-width,direction))
       
       
       
       
       
#internal used function#####

def cairo_context_to_pixel_array(surface):
    return np.ndarray(shape=(surface.get_width(),surface.get_height(),4),dtype=np.uint8,buffer=surface.get_data())

    
def view_from_array(pixel_array,file_name):
    surface=array2cairo(pixel_array)
    surface.write_to_png('{}.png'.format(file_name))
    if system()=='Linux':
        os.system('xdg-open {}.png'.format(file_name))

    
def interpolate_between_image(image1,image2,alpha):
    return np.mod((1-alpha)*buffer_of_image(image1)+alpha*buffer_of_image(image2),256).astype(np.uint8)


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
    
    
    
