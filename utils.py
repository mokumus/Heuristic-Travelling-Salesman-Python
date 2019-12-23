import copy
import random

import matplotlib.pyplot as plt


def random_permutation(array_like):
	perm = copy.deepcopy(array_like)
	for i in array_like:
		ri1 = random.randint(0, len(array_like) - 1)
		ri2 = random.randint(0, len(array_like) - 1)
		perm[ri1], perm[ri2] = perm[ri2], perm[ri1]
	return perm


def plot_tsp(path, points):
	# Modified from https://gist.github.com/payoung/6087046
	x = []
	y = []
	for i in range(0, len(points)):
		x.append(points[i][0])
		y.append(points[i][1])

	plt.plot(x, y, 'co')

	# Set a scale for the arrow heads
	a_scale = float(max(x)) / float(100)

	xi = []
	yi = []
	for j in path:
		xi.append(points[j-1][0])
		yi.append(points[j-1][1])

	plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]), head_width=a_scale, color='r', length_includes_head=True)
	for i in range(0, len(x) - 1):
		plt.arrow(xi[i], yi[i], (xi[i + 1] - xi[i]), (yi[i + 1] - yi[i]), head_width=a_scale, color='r', length_includes_head=True)

	# Set axis too slightly larger than the set of x and y
	plt.xlim(0, max(x) * 1.1)
	plt.ylim(0, max(y) * 1.1)
	plt.show()

