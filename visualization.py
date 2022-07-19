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


fig, axs = plt.subplots(1, 4)
fig.canvas.manager.set_window_title('Mit schönen Farben vom Meer damit es für Leo wie Heimat ist (weil Nordsee und so)')
ax1 = axs[0]
ax2 = axs[1]
ax3 = axs[2]
ax4= axs[3]


A, V=gc.new_generate_constraints(14,gc.Aes)
M, V=sf.d_var_to_beginning(A, V)
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