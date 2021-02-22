import os
def init_tex(tex_file,image_dir):
    if image_dir is not None:
        os.chdir(image_dir)
    tex=open(tex_file+'.tex','w')
    tex.write("\\documentclass[12pt]{article}\n")
    tex.write("\\usepackage{graphicx}\n")
    tex.write("\\begin{document}\n")
    tex.write("\\begin{figure}[h]\n")
    return tex


def make_tex(number_of_q,tex_file,image_dir):
    tex=init_tex(tex_file,image_dir)
    for i in range(1,number_of_q+1):
        tex.write("\\includegraphics[width=1.0\\textwidth]{"+str(i)+"}\n")
        tex.write("\\newline\n")
    tex.write("\\end{figure}\n")
    tex.write("\\end{document}")
    tex.close()

def compile_tex(number_of_q,tex_file="Question",image_dir=None):
    make_tex(number_of_q,tex_file,image_dir)
    status=os.system("xelatex {}.tex".format(tex_file))
    if not status:
        os.system("xdg-open {}.pdf".format(tex_file))
    else:
        print("tex file error")
