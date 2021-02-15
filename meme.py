
from plotlib.image import *


def modify_pixel(pixel_array,text,color,x0,y0,x,y,direction,border):
    if direction=='down':
        y0,y=y,y0
    surface=array2cairo(pixel_array)
    ctx=cairo.Context(surface)
    ctx.rectangle(x0,y0,x,y)
    ctx.set_source_rgba(*color)
    ctx.fill()
    ctx.set_source_rgba(*invert_color(color))
    ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(36)
    
    _, _, width, height,_,_= ctx.text_extents(text)
    height+=border
    if direction=='up':
        ctx.move_to(x/2-width/2,y/2+height/2)
    else:
        ctx.move_to(x/2-width/2,y0+height/2)   
    ctx.set_line_width(10)
    ctx.show_text(text)
    return cairo2array(surface)
      

def meme_template(image,text,width=80,color=[1,1,1,1],direction='up',border=20,file_name='meme_obj'):
    if isinstance(image,str):
        pixel_array=image2array(image)
    elif isinstance(image,np.ndarray) or isinstance(image,np.array):
        pixel_array=image
    else:
        print('Not valid image format')
        return None
    if direction =='up':
        array2image(modify_pixel(pixel_array,text,color,0,0,pixel_array.shape[0],width,direction,border),file_name)
    elif direction=='down':
        array2image(modify_pixel(pixel_array,text,color,0,pixel_array.shape[1],pixel_array.shape[0],pixel_array.shape[1]-width,direction,border),file_name)
       
       

  
