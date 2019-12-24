import copy
import utils
import tsplib95
import random
from timeit import default_timer as timer
from datetime import timedelta

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
		for i in range(0, neighborhood): 							# Generate neighbor, a neighborhood is a permutation that you can access in n number of two-opt's
			candidate_path = stochastic_two_opt(candidate_path)
		candidate_cost = utils.cost(candidate_path, problem)	 	# Calculate candidate cost after generating neighbour
		if candidate_cost < utils.cost(best_path, problem):
			count = 0
			best_path = candidate_path
	return best_path

## Perform VSN on the given problem
def search(problem, neighborhoods, max_no_improv, max_no_improv_ls):
	best_path = utils.random_permutation([*range(1, problem.dimension + 1, 1)]) # Create a random solution of problem size(number of cities)
	best_cost = utils.cost(best_path, problem)
	count = 0
	title = "Cost: {}, Time: {}, Err: %{:.4f}".format(best_cost, 0.0, utils.error_rate(problem.best_known, best_cost))
	utils.plot_tsp(best_path, problem, title)
	start = timer()

	while count <= max_no_improv:
		count += 1
		candidate_path = copy.deepcopy(best_path)
		for i in range(0, neighborhoods): # Generate neighbor, a neighborhood is a permutation that you can access in n number of two-opt's
			# Explore best_path's neighbours instead of random candidates neighbours
			# candidate_path = stochastic_two_opt(candidate_path)
			candidate_path = local_search(problem, best_path, max_no_improv_ls, i)
			candidate_cost = utils.cost(candidate_path, problem)
			if candidate_cost < best_cost:
				count = 0
				best_path = copy.deepcopy(candidate_path)
				best_cost = candidate_cost
				snapshot_timer(best_cost, best_path, problem, start)
				break
	snapshot_timer(best_cost, best_path, problem, start)
	return best_path

## pseudo real-time plotting wrapper for search method
def snapshot_timer(best_cost, best_path, problem, start):
	end = timer()
	elapsedTime = timedelta(seconds=end - start)
	title = "Cost: {}, Time: {}, Err: %{:.4f}".format(best_cost, elapsedTime.total_seconds(),
													  utils.error_rate(problem.best_known, best_cost))
	utils.plot_tsp(best_path, problem, title)


if __name__ == '__main__':
	problem = tsplib95.load_problem('problems/berlin52.tsp')
	problem.best_known = 7560
	search(problem, 12, 10, 65)

