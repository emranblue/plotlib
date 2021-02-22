import os


def init_tex(tex_file,image_dir):
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
        tex.write(f"\\includegraphics[width=1.0\textwidth]{i}\n")
    tex.write("\\end{figure}\n")
    tex.write("\\end{document}")
    tex.close()

def compile_tex(number_of_q,tex_file,image_dir):
    make_tex(number_of_q,tex_file,image_dir)
    status=os.system(f"xelatex {tex_file}.tex")
    if not status:
        os.system(f"xdg-open {tex_file}.pdf")
    else:
        print("tex file error")
