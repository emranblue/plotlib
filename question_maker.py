import os
PICTURE_DIR='/home/dbz/Pictures'
INIT_DIR=os.getcwd()
def make_ss_to_number():
    global PICTURE_DIR
    os.chdir(PICTURE_DIR)
    png_list=[]
    for fl in os.listdir(PICTURE_DIR):
        if fl.split('.')[-1]=='png':
            png_list.append(fl)
    return png_list
        
    
def remove_all():
    global PICTURE_DIR
    os.chdir(PICTURE_DIR)
    os.system("rm *.png")
    
def remove_tex():
    global INIT_DIR
    os.chdir(INIT_DIR)
    os.system("rm *.tex;rm *.log;rm *.aux")
    
def move_tex_file_init(tex_file):
    global INIT_DIR
    os.system("mv {}.pdf {}".format(tex_file,INIT_DIR))
    

def init_tex(tex_file,image_dir,title,time):
    global INIT_DIR,PICTURE_DIR
    if image_dir is not None:
        os.chdir(image_dir)
    iter_list=make_ss_to_number()
    tex=open(os.path.join(INIT_DIR,tex_file+'.tex'),'w')
    tex.write("\\documentclass[12pt]{article}\n")
    tex.write("\\usepackage{graphicx}\n")
    tex.write("\\graphicspath{{"+PICTURE_DIR+"/}}\n")
    tex.write("\\title{"+title+"}\n")
    tex.write("\\author{time-"+time+"}\n")
    tex.write("\\begin{document}\n")
    tex.write("\\maketitle\n")
   #tex.write("\\begin{figure}[ht]\n")
    return iter_list,tex


def make_tex(tex_file,image_dir,title,time):
    iter_list,tex=init_tex(tex_file,image_dir,title,time)
    for i,fl in enumerate(iter_list,start=1):
        if i%7==0:
            tex.write("\\newpage\n")
        tex.write("\\begin{figure}[ht]\n")
        tex.write("{}.\n".format(i))
        tex.write("\\break\n")
        tex.write("\\includegraphics[width=1.0\\textwidth]{"+str(fl)+"}\n")
        tex.write("\\break\n")
        tex.write("\\end{figure}\n")
    tex.write("\\end{document}")
    tex.close()

def compile_tex(title,time,tex_file=None,image_dir=None,remove=False,tex_remove=False):
    if not tex_file:
        tex_file=title+'_question'
    make_tex(tex_file,image_dir,title,time)
    print("Processing...")
    os.chdir(INIT_DIR)
    status=os.system("xelatex {}.tex > /dev/null".format(tex_file))
    print("Done.")
    if tex_remove:
        remove_tex()
    if not status:
        os.system("xdg-open {}.pdf > /dev/null".format(tex_file))
    else:
        print("tex file error")
    
    if remove:
        remove_all()
