import tsplib95
import utils

def main():
	problem = tsplib95.load_problem('problems/berlin52.tsp')

	my_path = [*range(1, problem.dimension + 1, 1)]
	r_path = utils.random_permutation(my_path)

	print(utils.cost(r_path, problem))
	utils.plot_tsp(r_path, problem)


if __name__ == '__main__': main()
