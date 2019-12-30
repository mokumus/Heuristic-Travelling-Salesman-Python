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
		if city != exclude and last_city != city:
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
	for choice in choices: # Choose city with highest probability
		v -= (choice['probability'] / p_sum)
		if v <= 0.0:
			return choice['city']

	return choices[-1]['city'] # Choose last city if no choice is made to this point



if __name__ == '__main__':
	problem = tsplib95.load_problem('problems/berlin52.tsp')
	problem.best_known = 7544.3659
	pheromon_map = initialise_pheromones(problem, 3.0)
	choices = calculate_choices(problem, 3, 1, pheromon_map, 0.9, 2.0)
	print(probabilistic_select(choices))


