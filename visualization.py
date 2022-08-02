from turtle import color
import matplotlib
from scipy.sparse import csr_matrix
import scipy.sparse as sparse
import generateConstraints as gc
import sortingFunctions as sf
import cipher as cip
import numpy as np
from pylatex import Document, Section, Figure, NoEscape, NewPage, Matrix, Math, Alignat, Command, Subsection
#matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as plt  # noqa
import matplotlib.pylab as plt
plt.rcParams.update({'font.size': 5})

def matplotlibvis(rounds, cipher):
    """
    Quick visualization without the hassle of generating the pdf file.
    """
    fig, axs = plt.subplots(1, 4)
    fig.canvas.manager.set_window_title('Mit schönen Farben vom Meer damit es für Leo wie Heimat ist (weil Nordsee und so)')
    ax1 = axs[0]
    ax2 = axs[1]
    ax3 = axs[2]
    ax4 = axs[3]


    A, V=gc.new_generate_constraints(rounds,cipher)
    M, v=sf.d_var_to_beginning(A, V)
    B=sf.long_constraints_to_top(M)
    C, W=sf.create_fourblock(A, V)

    axs[0].set_title('Native')
    axs[1].set_title('d_variables to the beginning')
    axs[2].set_title('long constraints to the top')
    axs[3].set_title('creating 4-block')

    ax1.spy(A, markersize=1, color="teal")
    ax2.spy(M, markersize=1, color="steelblue")
    ax3.spy(B, markersize=1, color="mediumturquoise")
    ax4.spy(C, markersize=1, color="skyblue")

    plt.show()

#matplotlibvis()

def matrix_to_latex_nonzero(A):
    """
    Generates the latex code for a csr_matrix while displaying only the nonzero values.
    (Can I optimize this? Currently going through every element(also nonzero))
    Parameters:
    ----------
    A       :   scr_matrix
                Sparse matrix that we want to display in a latex file

    Returns:
    ----------
    matri   :   string 
                Code for displaying the matrix
    """
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
    """
    Generates the code for the vector in the MILP.

    Parameters:
    ----------
    V       :   list
                List with all variablenames that we want to display in a latex file as a vector

    Returns:
    ----------
    vec     :   string 
                Code for displaying the vector
    """
    vec="\n \\begin{pmatrix}%\n"
    for i in V:
        vec = vec + i[0] + "_{" + i[1:] + "}\\\ \n"
    vec+="\end{pmatrix}%\n"
    return vec
    
def constraints(A,V):
    """
    Generates every constraint in a string.

    Parameters:
    ----------
    A       :   scr_matrix
                Sparse matrix that we want to multiply with the variablenames list

    V       :   list    
                Variablenames in a list, transposing this we get the vector to multiply the matrix with

    Returns:
    ----------
    cons    :   list of strings 
                Every element is the latexcode for the corresponding constraint
    """
    cons=[]
    for i in range(A.get_shape()[0]):
        #getting the indizes of the nonzero elements
        positions=A.getrow(i).nonzero()[1]
        con=""
        for e in positions:
            con=con+str(A[i,e])+V[e][0]+"_{"+V[e][1:]+"}+"
        #remove the last +
        con = con[:-1]
        con = con.replace("1x", "x")
        con = con.replace("1d", "d")
        con = con.replace("+-", "-")
        con+= "\geq 0"
        cons.append(con)
    return cons

def mainly(fname, width, A, V, title, *args, **kwargs):
    """
    Generates the pdf with the matrix, the structure and the constraints.
    """
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options)
    doc.preamble.append(Command("allowdisplaybreaks"))
    doc.preamble.append(Command("usepackage[labelformat=empty]{caption}"))
    doc.preamble.append(NoEscape("\setcounter{MaxMatrixCols}{10000}"))
    #doc.append(NoEscape("\\thispagestyle{empty}"))
    doc.preamble.append(NoEscape("\setlength{\headsep}{10pt}"))
    #doc.append(NoEscape("\setlength{\\footskip}{0pt}"))
    doc.preamble.append(NoEscape("\setlength{\\textheight}{650pt}"))
    doc.append(NoEscape("\setlength{\\voffset}{-0.50in}"))
    with doc.create(Section("Matrix Structure "+title[0]+", "+title[1]+" rounds")):
        with doc.create(Figure(position='h!p')) as plot:
            plot.add_plot(width=460, *args, **kwargs)

    doc.append(NewPage())
    with doc.create(Section("MILP")): #HERE ÄNDERN
        doc.append(NoEscape("\\resizebox{\linewidth}{!}{%\n" + matrix_to_latex_nonzero(A)+vectormilp(V)+"}\n\geq 0"))
    
    doc.append(NewPage())
    with doc.create(Section("Constraints")):
        B=constraints(A,V)
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            for i in B:
                agn.append(i+"\\\\")
    
    doc.generate_pdf(clean_tex=False)



def gen_pdf(cipher, rounds):  
    fig, axs = plt.subplots(2, 2, figsize=(6,8))
    ax1 = axs[0][0]
    ax2 = axs[0][1]
    ax3 = axs[1][0]
    ax4 = axs[1][1]
    
    A, V=gc.new_generate_constraints(rounds,cipher)
    M, v=sf.d_var_to_beginning(A, V)
    B=sf.long_constraints_to_top(M)
    C, W=sf.create_fourblock(A, V)

    ax1.set_title('native')
    ax2.set_title('d_variables to the left')
    ax3.set_title('long constraints to the top')
    ax4.set_title('creating 4-block')

    ax1.spy(A, markersize=1, color="teal")
    ax2.spy(M, markersize=1, color="steelblue")
    ax3.spy(B, markersize=1, color="mediumturquoise")
    ax4.spy(C, markersize=1, color="skyblue") 

    title=[str(cipher)[15:-2],str(rounds)]
    mainly(title[0]+title[1]+'rounds', r'1\textwidth', A=A, V=V, title=title, dpi=300)
    #main funktkion anders bennenen und das hier auch in eine Funktion rein
    #jetzt noch die anderen Sachen mitrein (matrix und constraints und dann main funktion verändern)

#gen_pdf(cip.Aes,20)

    