import tsplib95
import utils






def main():
	problem = tsplib95.load_problem('problems/kroA100.tsp')

	my_points = []
	for i in range(1, problem.dimension + 1):
		my_points.append(problem.node_coords[i])

	my_path = [*range(1, problem.dimension + 1, 1)]

	utils.plot_tsp(utils.random_permutation(my_path), my_points)
	utils.plot_tsp(utils.random_permutation(my_path), my_points)

if __name__ == '__main__': main()
