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

if __name__ == '__main__':
	problem = tsplib95.load_problem('problems/berlin52.tsp')
	problem.best_known = 7544.3659
	pheromone_map = initialise_pheromones(problem, 3.0)
	stepwise_const(problem, pheromone_map, 2.5, 0.9)
	perm = utils.random_permutation([*range(1, problem.dimension + 1)])
	print(perm)
	global_update_pheromone(problem,pheromone_map,perm, 0.1)



