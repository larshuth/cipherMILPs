from turtle import color
import matplotlib.pylab as plt
from scipy.sparse import csr_matrix
import scipy.sparse as sparse
import generateConstraints as gc
import sortingFunctions as sf
import numpy as np
"""
still in the making
using this file to somehow visualize them (not final)
"""

def matplotlibvis():
    fig, axs = plt.subplots(1, 4)
    fig.canvas.manager.set_window_title('Mit schönen Farben vom Meer damit es für Leo wie Heimat ist (weil Nordsee und so)')
    ax1 = axs[0]
    ax2 = axs[1]
    ax3 = axs[2]
    ax4 = axs[3]


    A, V=gc.new_generate_constraints(50,gc.Enocoro)
    M, v=sf.d_var_to_beginning(A, V)
    B=sf.long_constraints_to_top(M)
    C=sf.create_fourblock(A, V)

    axs[0].set_title('Native')
    axs[1].set_title('d_variables to the beginning')
    axs[2].set_title('long constraints to the top')
    axs[3].set_title('creating 4-block')

    ax1.spy(A, markersize=1, color="teal")
    ax2.spy(M, markersize=1, color="steelblue")
    ax3.spy(B, markersize=1, color="mediumturquoise")
    ax4.spy(C, markersize=1, color="skyblue")

    plt.show()

from pylatex import Document, Section, Figure, NoEscape, NewPage, Matrix, Math, Alignat, Command

#matplotlib.use('Agg')   Not to use X server. For TravisCI.
import matplotlib.pyplot as plt  # noqa

def sparsemath(A):
    A=A.toarray()
    matri= "\\begin{pmatrix}%\n"
    for i in range(len(A)):
        for j in range(len(A[i])):
            if j!=0:
                matri+="&"
            if A[i][j]!=0:
                matri+=str(A[i][j])
        matri+="\\\ \n"
    matri+="\end{pmatrix}%\n"
    return matri

def vectormilp(V):
    vec="\n \\begin{pmatrix}%\n"
    for i in V:
        vec = vec + i[0] + "_{" + i[1:] + "}\\\ \n"
    vec+="\end{pmatrix}%\n"
    return vec
    
def constraints(A,V):
    """
    output: liste mit strings die die gleichungen sind
    """
    #getting the indizes of the nonzero elements
    cons=[]
    for i in range(A.get_shape()[0]):
        positions=A.getrow(i).nonzero()[1]
        con=""
        for e in positions:
            con=con+str(A[i,e])+V[e][0]+"_{"+V[e][1:]+"}+"
        #remove the last +
        con=con[:-1]
        con+= "\geq 0"
        cons.append(con)
    return cons

def main(fname, width, A, V, *args, **kwargs):
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options)
    doc.preamble.append(Command("allowdisplaybreaks"))
    doc.append(NoEscape("\setcounter{MaxMatrixCols}{1000}"))

    with doc.create(Section('Sparse Matrix Structure')):
        with doc.create(Figure(position='htbp')) as plot:
            plot.add_plot(width=NoEscape(width), *args, **kwargs)
            plot.add_caption('Created using matplotlib.')

    doc.append(NewPage())
    mat=Matrix(A.toarray())
    #math = Math(data=['M=', mat])
    #doc.append(math)
    
    with doc.create(Section("MILP")):
        doc.append(NoEscape("\\resizebox{\linewidth}{!}{%\n" + sparsemath(A)+vectormilp(V)+"}\n\geq 0"))
    doc.append(NewPage())
    with doc.create(Section("Constraints")):
        B=constraints(A,V)
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            for i in B:
                agn.append(i+"\\\\")

    doc.generate_pdf(clean_tex=False)

#C:/Users/Sofia Lohr/AppData/Local/Programs/MiKTeX/miktex/bin/x64/latexmk
#C:/Users/Sofia Lohr/AppData/Local/Programs/MiKTeX/scripts/latexmk/latexmk"
#C:/Users/Sofia Lohr/AppData/Local/Programs/MiKTeX/latexmk.py
#C:\Users\Sofia Lohr\AppData\Local\Programs\MiKTeX
#C:/Users/Sofia Lohr/AppData/Local/Programs/Python/Python38/Lib/site-packages/pdflatex/pdflatex
#Programs\MiKTeX\miktex\bin\x64
#C:/Users/Sofia Lohr/AppData/Local/Programs/Python/Python38/Scripts/latexmk.py-script

if __name__ == '__main__':
    
    fig, axs = plt.subplots(1, 2)
    ax1 = axs[0]
    ax2 = axs[1]
    A, V=gc.new_generate_constraints(5,gc.Aes)
    M, W=sf.create_fourblock(A, V)
    ax1.spy(A, markersize=1, color="teal")
    ax2.spy(M, markersize=1, color="mediumturquoise")
    axs[0].set_title('Native')
    axs[1].set_title('Creating 4-block')

    main('matplotlib_ex-dpi', r'1\textwidth', A=A, V=V, dpi=300)
    #main('matplotlib_ex-facecolor', r'0.5\textwidth', facecolor='b')

    