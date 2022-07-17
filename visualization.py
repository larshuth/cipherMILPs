import matplotlib.pylab as plt
from scipy.sparse import csr_matrix
import scipy.sparse as sparse
import generateConstraints as gc
"""
still in the making
using this file to somehow visualize them (not final)
"""

A=gc.new_generate_constraints(7,gc.Enocoro)
plt.spy(A, markersize=1)


plt.show()