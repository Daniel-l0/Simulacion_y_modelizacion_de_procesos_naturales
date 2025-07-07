import sys
import numpy as np
import matplotlib.pyplot as plt

fname_in = sys.argv[1]
fname_out = sys.argv[2]
pos = np.loadtxt(fname_in)
ax = plt.gcf().add_subplot(111, aspect='equal')
ax.cla()
ax.scatter(pos[:,0], pos[:,1], 1)
ax.set_xlim([0., 1.0])
ax.set_ylim([0., 1.0])
plt.gcf().savefig(fname_out)
