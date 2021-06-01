
from image import *


def modify_pixel(pixel_array,text,bg_color,text_color,x0,y0,x,y,direction,border,font,font_size):
    if direction=='down':
        y0,y=y,y0
    surface=array2cairo(pixel_array)
    ctx=cairo.Context(surface)
    ctx.rectangle(x0,y0,x,y)
    ctx.set_source_rgba(*bg_color)
    ctx.fill()
    ctx.set_source_rgba(*text_color)
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(font_size)
    
    _, _, width, height,_,_= ctx.text_extents(text)
    height+=border
    if direction=='up':
        ctx.move_to(x/2-width/2,y/2+height/2)
    else:
        ctx.move_to(x/2-width/2,y0+height/2)   
    ctx.set_line_width(10)
    ctx.show_text(text)
    return cairo2array(surface)
      

def meme_template(image,text,width=80,bg_color=[1,1,1,1],text_color=[0,0,0,1],direction='down',border=20,file_name='meme_obj'):
    if isinstance(image,str):
        pixel_array=image2array(image)
    elif isinstance(image,np.ndarray) or isinstance(image,np.array):
        pixel_array=image
    else:
        print('Not valid image format')
        return None
    if direction =='up':
        array2image(modify_pixel(pixel_array,text,bg_color,text_color,0,0,pixel_array.shape[0],width,direction,border),file_name)
    elif direction=='down':
        array2image(modify_pixel(pixel_array,text,bg_color,text_color,0,pixel_array.shape[1],pixel_array.shape[0],pixel_array.shape[1]-width,direction,border),file_name)


def meme2array(pixel_array,caption,width=80,bg_color=[1,1,1,1],text_color=[0,0,0,1],direction='down',border=30,font="Peace Sans",font_size=36):
    if direction =='up':
        return modify_pixel(pixel_array,caption,bg_color,text_color,0,0,pixel_array.shape[1],width,direction,border,font,font_size)
    elif direction=='down':
        return modify_pixel(pixel_array,caption,bg_color,text_color,0,pixel_array.shape[0],pixel_array.shape[1],pixel_array.shape[0]-width,direction,border,font,font_size)




       

  
