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


def cost(path, problem):
	cities = problem.node_coords
	total_cost = 0
	for i in range(0, len(path) - 1):
		total_cost += problem.wfunc(path[i], path[i + 1])
	return total_cost


def plot_tsp(path, problem):
	# Modified from https://gist.github.com/payoung/6087046
	cities = []
	x = []
	y = []
	for i in range(1, problem.dimension + 1):
		cities.append(problem.node_coords[i])

	for i in range(0, len(cities)):
		x.append(cities[i][0])
		y.append(cities[i][1])

	plt.plot(x, y, 'co')

	# Set a scale for the arrow heads
	a_scale = float(max(x)) / float(100)

	xi = []
	yi = []
	for j in path:
		xi.append(cities[j - 1][0])
		yi.append(cities[j - 1][1])

	plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]), head_width=a_scale, color='r', length_includes_head=True)
	for i in range(0, len(x) - 1):
		plt.arrow(xi[i], yi[i], (xi[i + 1] - xi[i]), (yi[i + 1] - yi[i]), head_width=a_scale, color='r', length_includes_head=True)

	# Set axis too slightly larger than the set of x and y
	plt.xlim(0, max(x) * 1.1)
	plt.ylim(0, max(y) * 1.1)
	plt.show()

