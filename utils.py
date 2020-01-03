import copy
import math
import random

import matplotlib.pyplot as plt


def error_rate(accepted, experimental):
	return math.fabs(accepted - experimental) / accepted * 100

def random_permutation(array_like):
	perm = copy.deepcopy(array_like)
	for _ in array_like:
		ri1 = random.randint(0, len(array_like) - 1)
		ri2 = random.randint(0, len(array_like) - 1)
		perm[ri1], perm[ri2] = perm[ri2], perm[ri1]
	return perm

def cost(path, problem):
	total_cost = 0
	for i in range(0, len(path) - 1):
		total_cost += problem.wfunc(path[i], path[i + 1])
	total_cost += problem.wfunc(path[-1], path[0])	#complete loop
	return total_cost

def simple_log(problem, elapsedTime, best_cost, best_path, initial_cost):
	print("\nMinimized cost: {}".format(best_cost))
	print("Err: %{:.4f}".format(error_rate(problem.best_known, best_cost)))
	print("Time : {}".format(elapsedTime.total_seconds()))
	print("Path: {}".format(best_path))
	print("="*140)
	print("="*140)
	str_ = "{:.5f} {:.1f} {:.1f} {:.4f}".format(elapsedTime.total_seconds(), initial_cost, best_cost, error_rate(problem.best_known, best_cost))
	return str_

def plot_tsp(path, problem, str = ""):
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
	plt.title(str)
	# Set a scale for the arrow heads
	a_scale = float(max(x)) / float(100)

	xi = []
	yi = []
	for j in path:
		xi.append(cities[j - 1][0])
		yi.append(cities[j - 1][1])

	plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]), head_width=a_scale, color='g', length_includes_head=True)
	for i in range(0, len(x) - 1):
		plt.arrow(xi[i], yi[i], (xi[i + 1] - xi[i]), (yi[i + 1] - yi[i]), head_width=a_scale, color='r', length_includes_head=True)

	# Set axis too slightly larger than the set of x and y
	plt.xlim(0, max(x) * 1.1)
	plt.ylim(0, max(y) * 1.1)
	plt.show()

