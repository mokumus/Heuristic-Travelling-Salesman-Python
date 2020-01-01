import random
import utils
import vns
import tsplib95
from timeit import default_timer as timer
from datetime import timedelta

def initialise_pheromones(problem, init_pher) :
	pheromone_map = {}
	for edge in list(problem.get_edges()):
		pheromone_map[edge] = init_pher
	return pheromone_map

def calculate_choices(problem, last_city, exclude, pheromone_map, c_heur, c_hist):
	choices = []
	for city in problem.get_nodes():
		if city not in exclude:
			p = dict()
			p['city']       = city
			p['history']    = pheromone_map[(last_city,city)] ** c_hist
			p['distance']   = problem.wfunc(last_city, city)
			p['heuristic']  = (1.0/p['distance']) ** c_heur
			p['probability']= p['history'] * p['heuristic']
			choices.append(p)
	return choices

def probabilistic_select(choices) :
	p_sum = sum([choice['probability'] for choice in choices])

	if p_sum == 0.0:  # Choose random city in case of no sum
		return choices[random.randint(0,len(choices))]['city']

	v = random.random()
	for choice in choices: # Choose good city near a high probability city
		v -= choice['probability'] / p_sum
		if v <= 0.0:
			return choice['city']

	return choices[-1]['city'] # Choose last city if no choice is made to this point

def greedy_select(choices) :
	return max(choices, key=lambda x:x['probability'])['city']  # Choose city with highest probability

def stepwise_const(problem, pheromone_map, c_heur, c_greed) :
	perm = [random.randint(1, problem.dimension)] # Start path at random point

	while len(perm) < problem.dimension :
		choices = calculate_choices(problem, perm[-1], perm, pheromone_map, c_heur, 1.0)
		is_greedy = random.random() <= c_greed
		next_city = greedy_select(choices) if is_greedy else probabilistic_select(choices)
		perm.append(next_city)
	return perm

def global_update_pheromone(problem, pheromone_map, candidate_path, decay_amount) :
	for i in range(0,len(candidate_path)-1):
		edge_forward = (candidate_path[i], candidate_path[i+1])
		edge_back    = (candidate_path[i+1], candidate_path[i])
		value = ((1.0 - decay_amount) * pheromone_map[edge_forward]) + (decay_amount * (1.0 / utils.cost(candidate_path,problem)))
		pheromone_map[edge_forward] = value
		pheromone_map[edge_back]	= value

def local_update_pheromone(pheromone_map, candidate_path, c_local_pher, init_pher) :
	for i in range(0,len(candidate_path)-1):
		edge_forward = (candidate_path[i], candidate_path[i+1])
		edge_back    = (candidate_path[i+1], candidate_path[i])
		value = ((1.0 - c_local_pher) * pheromone_map[edge_forward]) + (c_local_pher * init_pher)
		pheromone_map[edge_forward] = value
		pheromone_map[edge_back]	= value

def search(problem, max_iters, num_ants, decay_amount, c_heur, c_local_pher, c_greed) :
	best_path = problem.initial_path
	best_cost = utils.cost(best_path,problem)
	initial_cost = best_cost
	init_pheromone = 1.0 / (problem.dimension * best_cost)
	pheromone_map = initialise_pheromones(problem, init_pheromone)

	start = timer()
	print("Initial cost: {}".format(best_cost))
	print("ACO: ", end="")
	for _ in range(0, max_iters):
		print("#", end="")
		for _ in range(0, num_ants):
			candidate_path = stepwise_const(problem,pheromone_map,c_heur,c_greed)
			candidate_cost = utils.cost(candidate_path,problem)
			if candidate_cost < best_cost:
				best_path = candidate_path
				best_cost = candidate_cost
				local_update_pheromone(pheromone_map, candidate_path, c_local_pher, init_pheromone)
		global_update_pheromone(problem,pheromone_map,candidate_path,decay_amount)

	end = timer()
	elapsedTime = timedelta(seconds=end - start)
	csv_log_str = utils.simple_log(problem, elapsedTime, best_cost, best_path, initial_cost)

	return best_path, csv_log_str

def acols(problem, max_iters, num_ants, decay_amount, c_heur, c_local_pher, c_greed) :
	best_path = problem.initial_path
	best_cost = utils.cost(best_path,problem)
	initial_cost = best_cost
	init_pheromone = 1.0 / (problem.dimension * best_cost)
	pheromone_map = initialise_pheromones(problem, init_pheromone)

	start = timer()
	print("Initial cost: {}".format(best_cost))
	print("ACO: ", end="")
	for _ in range(0, max_iters):
		print("#", end="")
		for _ in range(0, num_ants):
			candidate_path = stepwise_const(problem,pheromone_map,c_heur,c_greed)
			candidate_cost = utils.cost(candidate_path,problem)
			ls_path = vns.local_search(problem,best_path,10,6)
			ls_cost = utils.cost(ls_path, problem)

			if ls_cost < candidate_cost:
				candidate_path = ls_path
				candidate_cost = ls_cost

			if candidate_cost < best_cost:
				best_path = candidate_path
				best_cost = candidate_cost
				local_update_pheromone(pheromone_map, candidate_path, c_local_pher, init_pheromone)
		global_update_pheromone(problem,pheromone_map,candidate_path,decay_amount)

	end = timer()
	elapsedTime = timedelta(seconds=end - start)
	csv_log_str = utils.simple_log(problem, elapsedTime, best_cost, best_path, initial_cost)

	return best_path, csv_log_str


if __name__ == '__main__':
	problem_berlin52 = tsplib95.load_problem('problems/berlin52.tsp')
	problem_berlin52.best_known = 7544.3659
	problem_berlin52.initial_path = utils.random_permutation([*range(1, problem_berlin52.dimension + 1, 1)])


	s, _= search(problem_berlin52, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9)
	utils.plot_tsp(s,problem_berlin52)

	s, _= acols(problem_berlin52, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9)
	utils.plot_tsp(s,problem_berlin52)



