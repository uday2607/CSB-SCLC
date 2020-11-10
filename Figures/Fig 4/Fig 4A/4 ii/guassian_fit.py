import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
import os, pickle
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.interpolate import interpn

def density_scatter(x, y, xlabel, ylabel, sort = True, bins = [20,20], **kwargs):

	"""
	Scatter plot colored by 2d histogram
	"""

	fig , ax = plt.subplots()
	data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True)
	z = interpn((0.5*(x_e[1:] + x_e[:-1]),0.5*(y_e[1:]+y_e[:-1])) ,data ,np.vstack([x,y]).T ,method = "splinef2d", bounds_error = False)

	#To be sure to plot all data
	z[np.where(np.isnan(z))] = 0.0

	# Sort the points by density, so that the densest points are plotted last
	if sort :
		idx = z.argsort()
		x, y, z = x[idx], y[idx], z[idx]

	ax.scatter(x, y, s = 5, c=z, **kwargs)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)

	norm = Normalize(vmin = np.min(z), vmax = np.max(z))
	cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
	cbar.ax.set_ylabel('Density')

	plt.suptitle("Scatter plot of ASCL1 and NEUROD1")
	plt.savefig("Scatter_plot_A_and_N.png")
	plt.close()

if __name__ == '__main__':

	df = pickle.load(open("racipe_up1.data",'rb'))
	nodes = list(df.index)
	scaled_data = preprocessing.scale(df.T)
	data_A = scaled_data[:, nodes.index("ASCL1")]
	data_N = scaled_data[:, nodes.index("NEUROD1")]

	density_scatter(data_A, data_N, 'ASCL1', 'NEUROD1',bins=[200,200])
