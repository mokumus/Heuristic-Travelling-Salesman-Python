import copy
import utils
import tsplib95
import random
import csv
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
def search(problem, neighborhoods, max_no_improv, max_no_improv_ls, plot_progress = False, plot_end_start = False):
	best_path = utils.random_permutation([*range(1, problem.dimension + 1, 1)]) # Create a random solution of problem size(number of cities)
	best_cost = utils.cost(best_path, problem)
	initial_cost = best_cost
	count = 0
	if plot_end_start:
		title = "Cost: {}, Time: {}, Err: %{:.4f}".format(best_cost, 0.0, utils.error_rate(problem.best_known, best_cost))
		utils.plot_tsp(best_path, problem, title)
	start = timer()
	print("Initial cost: {}".format(best_cost))
	print("VNS: ", end="")
	while count <= max_no_improv:
		print("#", end="")
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
				if plot_progress:
					snapshot_timer(best_cost, best_path, problem, start)
				break
	end = timer()
	elapsedTime = timedelta(seconds=end - start)
	if plot_end_start:
		snapshot_timer(best_cost, best_path, problem, start)
	print("\nMinimized cost: {}".format(best_cost))
	print("Err: %{:.4f}".format(utils.error_rate(problem.best_known, best_cost)))
	print("Time : {}".format(elapsedTime.total_seconds()))
	print("Path: {}".format(best_path))
	csv_log_str = "{:.5f} {:.1f} {:.1f} {:.4f}".format(elapsedTime.total_seconds(), initial_cost, best_cost,utils.error_rate(problem.best_known, best_cost))
	return best_path, csv_log_str

## pseudo real-time plotting wrapper for search method
def snapshot_timer(best_cost, best_path, problem, start):
	end = timer()
	elapsedTime = timedelta(seconds=end - start)
	title = "Cost: {}, Time: {}, Err: %{:.4f}".format(best_cost, elapsedTime.total_seconds(),
													  utils.error_rate(problem.best_known, best_cost))
	utils.plot_tsp(best_path, problem, title)


def test_berlin52(file_name, number_of_runs = 1, n = 12, mni = 10, mnils = 65, pp=False, pes=False):
	with open(file_name, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["NEIGHBORHOODS:    {}".format(n)])
		writer.writerow(["MAX_NO_IMPROV:    {}".format(mni)])
		writer.writerow(["MAX_NO_IMPROV_LS: {}".format(mnils)])
		writer.writerow(["NUMBER OF RUNS:   {}".format(number_of_runs)])
		writer.writerow(["Time", "Initial Cost","Minimized Cost", "Error Rate"])
		for i in range(0, number_of_runs):
			_ , csv_str = search(problem, neighborhoods=n, max_no_improv=mni, max_no_improv_ls=mnils, plot_progress=pp, plot_end_start=pes)
			writer.writerow(csv_str.split())


if __name__ == '__main__':
	problem = tsplib95.load_problem('problems/berlin52.tsp')
	problem.best_known = 7560

	test_berlin52(file_name='results/berlin52_sol.csv', number_of_runs=1, mnils=10, pp=False, pes=False)
