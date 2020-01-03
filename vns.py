import copy
import random
from datetime import timedelta
from timeit import default_timer as timer

import tsplib95

import utils


## Reverse path between two random points
def stochastic_two_opt(path):
	perm = copy.deepcopy(path)
	i = random.randint(0, len(perm) - 1)
	j = random.randint(0, len(perm) - 1)
	if i > j:
		i, j = j, i
	perm[i:j + 1] = list(reversed(perm[i:j + 1]))
	return perm

## Perform local search on the given problem
## Generate neighbors w.r.t neighborhood
## Update best_path if a neighbor is global best
## Else don't touch best_path
def local_search(problem, best_path , max_no_improv, neighborhood):
	count = 0
	while count <= max_no_improv:
		count += 1
		candidate_path = copy.deepcopy(best_path)
		for i in range(0, neighborhood):						# Generate neighbor, a neighborhood is a permutation that you can access in n number of two-opt's
			candidate_path = stochastic_two_opt(candidate_path)
		candidate_cost = utils.cost(candidate_path, problem)	# Calculate candidate cost after generating neighbour
		if candidate_cost < utils.cost(best_path, problem):
			count = 0
			best_path = candidate_path
	return best_path

## Perform VSN on the given problem
## Default values are determined by testing on berlin52 data set
def search(problem, neighborhoods=6, max_no_improv=40, max_no_improv_ls=20, plot_progress = False, plot_end_start = False):
	best_path = utils.random_permutation([*range(1, problem.dimension + 1, 1)]) # Create a random solution of problem size(number of cities)
	best_cost = utils.cost(best_path, problem)
	initial_cost = best_cost
	count = 0
	start = timer()
	print("Initial cost: {}".format(best_cost))
	print("AVNS: ", end="")
	while count <= max_no_improv:
		count += 1
		for i in range(0, neighborhoods): # Generate neighbor, a neighborhood is a permutation that you can access in n number of two-opt's
			# Explore best_path's neighbours instead of random candidates neighbours
			candidate_path = local_search(problem, best_path, max_no_improv_ls, i)
			candidate_cost = utils.cost(candidate_path, problem)
			if candidate_cost < best_cost:
				print("#", end="")  # Search progress
				count = 0
				best_path = copy.deepcopy(candidate_path)
				best_cost = candidate_cost
				break
	end = timer()
	elapsedTime = timedelta(seconds=end - start)
	csv_log_str = utils.simple_log(problem, elapsedTime, best_cost, best_path, initial_cost)

	return best_path, csv_log_str

def vns_dynamic(problem, c_divr = 0.4, max_iter=60000, neighborhoods=12, max_no_improv=40, max_no_improv_ls=20, plot_progress = False, plot_end_start = False):
	best_path = utils.random_permutation([*range(1, problem.dimension + 1, 1)]) # Create a random solution of problem size(number of cities)
	best_cost = utils.cost(best_path, problem)
	initial_cost = best_cost
	count = 0
	m = 0

	start = timer()
	print("Initial cost: {}".format(best_cost))
	print("VNS: ", end="")
	while count <= max_no_improv and m < max_iter:

		for i in range(0, neighborhoods):  # Generate neighbor, a neighborhood is a permutation that you can access in n number of two-opt's
			m += max_no_improv_ls
			if m <= (int(max_iter*c_divr)):
				candidate_path = stochastic_two_opt(best_path)
			else:
				candidate_path = copy.deepcopy(best_path)
			candidate_path = local_search(problem, candidate_path, max_no_improv_ls, i)
			candidate_cost = utils.cost(candidate_path, problem)
			if candidate_cost < best_cost:
				print("#", end="")  # Search progress
				count = 0
				m -= max_no_improv_ls
				best_path = copy.deepcopy(candidate_path)
				best_cost = candidate_cost
				break
	end = timer()
	elapsedTime = timedelta(seconds=end - start)

	csv_log_str = utils.simple_log(problem, elapsedTime, best_cost, best_path, initial_cost)
	return best_path, csv_log_str


if __name__ == '__main__':
	problem_berlin52 = tsplib95.load_problem('problems/berlin52.tsp')
	problem_berlin52.best_known = 7544.3659
	vns_dynamic(problem_berlin52, c_divr=0.4, neighborhoods=6, max_no_improv=40, max_no_improv_ls=20, plot_progress=True, plot_end_start=True)


