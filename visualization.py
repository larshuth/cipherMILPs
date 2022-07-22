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

"""
fig, axs = plt.subplots(1, 4)
fig.canvas.manager.set_window_title('Mit schönen Farben vom Meer damit es für Leo wie Heimat ist (weil Nordsee und so)')
ax1 = axs[0]
ax2 = axs[1]
ax3 = axs[2]
ax4 = axs[3]


A, V=gc.new_generate_constraints(50,gc.Enocoro)
M, V=sf.create_fourblock(A, V)
#M, V=sf.d_var_to_beginning(A, V)
B=sf.long_constraints_to_top(M)
C=sf.creating_diagonal_in4block(B, V)

axs[0].set_title('Native')
axs[1].set_title('d_variables to the beginning')
axs[2].set_title('long constraints to the top')
axs[3].set_title('creating the diagonal')

ax1.spy(A, markersize=1, color="teal")
ax2.spy(M, markersize=1, color="steelblue")
ax3.spy(B, markersize=1, color="mediumturquoise")
ax4.spy(C, markersize=1, color="skyblue")

plt.show()
"""
import matplotlib

from pylatex import Document, Section, Figure, NoEscape

#matplotlib.use('Agg')   Not to use X server. For TravisCI.
import matplotlib.pyplot as plt  # noqa


def main(fname, width, *args, **kwargs):
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options)

    doc.append('Introduction.')

    with doc.create(Section('I am a section')):
        doc.append('Take a look at this beautiful plot:')

        with doc.create(Figure(position='htbp')) as plot:
            plot.add_plot(width=NoEscape(width), *args, **kwargs)
            plot.add_caption('I am a caption.')

        doc.append('Created using matplotlib.')

    doc.append('Conclusion.')

    doc.generate_pdf(clean_tex=False)

#C:/Users/Sofia Lohr/AppData/Local/Programs/MiKTeX/miktex/bin/x64/latexmk
#C:/Users/Sofia Lohr/AppData/Local/Programs/MiKTeX/scripts/latexmk/latexmk"
#C:/Users/Sofia Lohr/AppData/Local/Programs/MiKTeX/latexmk.py
#C:\Users\Sofia Lohr\AppData\Local\Programs\MiKTeX
#C:/Users/Sofia Lohr/AppData/Local/Programs/Python/Python38/Lib/site-packages/pdflatex/pdflatex
#Programs\MiKTeX\miktex\bin\x64
#C:/Users/Sofia Lohr/AppData/Local/Programs/Python/Python38/Scripts/latexmk.py-script

if __name__ == '__main__':
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]
    
    A, V=gc.new_generate_constraints(50,gc.Enocoro)
    M, V=sf.create_fourblock(A, V)
    plt.spy(M, markersize=1)

    main('matplotlib_ex-dpi', r'1\textwidth', dpi=300)
    main('matplotlib_ex-facecolor', r'0.5\textwidth', facecolor='b')

    