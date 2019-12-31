import copy
import random
import utils
import tsplib95

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
	best_path = [*range(1, problem.dimension + 1, 1)]
	best_cost = utils.cost(best_path,problem)
	init_pheromone = 1.0 / (problem.dimension * best_cost)
	pheromone_map = initialise_pheromones(problem, init_pheromone)
	for _ in range(0, max_iters):
		solutions = []
		for _ in range(0, num_ants):
			candidate_path = stepwise_const(problem,pheromone_map,c_heur,c_greed)
			candidate_cost = utils.cost(candidate_path,problem)
			if candidate_cost < best_cost:
				best_path = candidate_path
				best_cost = candidate_cost
				local_update_pheromone(pheromone_map, candidate_path, c_local_pher, init_pheromone)
		global_update_pheromone(problem,pheromone_map,candidate_path,decay_amount)
	print(best_path)
	print(best_cost)
	return best_path


if __name__ == '__main__':
	problem = tsplib95.load_problem('problems/kroA100.tsp')
	problem.best_known = 7544.3659

	search(problem, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9)



