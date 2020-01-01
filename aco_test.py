import aco
import csv
import utils
import tsplib95
from datetime import datetime

def test_aco(file_name, problem, max_iters, num_ants, decay_amount, c_heur, c_local_pher, c_greed, number_of_runs=1):
	info = [0,float('inf'),0,0,float('inf')]
	file_path = "results/"
	file_path +=file_name
	file_path += ".csv"
	with open(file_path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Time", "Initial Cost", "Minimized Cost", "Error Rate"])
		for i in range(0, number_of_runs):
			_ , csv_str = aco.acols(problem, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9)
			tmp = csv_str.split()
			info[0] += float(tmp[0])				#AVG_TIME
			info[1] =  min(float(tmp[2]),info[1])	#AVG_COST
			info[2] += float(tmp[2])				#TOTAL_COST
			info[3] += float(tmp[3])				#TOTAL_ERR
			info[4] =  min(float(tmp[3]),info[4]) 	#MIN_ERR
			writer.writerow(csv_str.split(" "))

		writer.writerow(["AVG TIME", info[0]/number_of_runs])
		writer.writerow(["MIN_COST", info[1]])
		writer.writerow(["AVG_COST", info[2]/number_of_runs])
		writer.writerow(["MIN_ERR ",  info[4]])
		writer.writerow(["AVG_ERR ", info[3]/number_of_runs])
		writer.writerow(["MAX_ITERS", max_iters])
		writer.writerow(["#ANTS", num_ants])
		writer.writerow(["DECAY", decay_amount])
		writer.writerow(["C_LOCAL_PHER", c_local_pher])
		writer.writerow(["C_HEUR", c_heur])
		writer.writerow(["C_GREED", c_greed])




def run_tests1(file_name, p):
	#MAX ITER TESTS
	test_aco(file_name, p, max_iters=50, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=75, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)

	#NUMBER OF ANTS TESTS
	test_aco(file_name, p, max_iters=100, num_ants=5, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=8, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)

	#DECAY AMOUNT TESTS
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.0, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.2, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.4, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.6, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)

	#C_HEUR TESTS
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=0.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=1.0, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.0, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=3.0, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=3.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)

	#C_LOCAL_PHER TESTS
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.2, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.3, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=0.9, number_of_runs=20) #BEST RESULT
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.5, c_greed=0.9, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.6, c_greed=0.9, number_of_runs=20)

	#C_GREED TESTS
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=0.5, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=1.0, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=1.5, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=2.5, number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=10, decay_amount=0.1, c_heur=2.5, c_local_pher=0.1, c_greed=3.0, number_of_runs=20)

def run_tests2(file_name, p):
	#MAX ITER & GREED TESTS
	test_aco(file_name, p, max_iters=50, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=0.9,number_of_runs=20)
	test_aco(file_name, p, max_iters=50, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=1.0,number_of_runs=20)
	test_aco(file_name, p, max_iters=50, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=3.0,number_of_runs=20)

	test_aco(file_name, p, max_iters=100, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=0.9,number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=1.0,number_of_runs=20)
	test_aco(file_name, p, max_iters=100, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=3.0,number_of_runs=20)

	test_aco(file_name, p, max_iters=150, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=0.9,number_of_runs=20)
	test_aco(file_name, p, max_iters=150, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=1.0, number_of_runs=20)
	test_aco(file_name, p, max_iters=150, num_ants=12, decay_amount=0.1, c_heur=2.5, c_local_pher=0.4, c_greed=3.0, number_of_runs=20)


if __name__ == '__main__':

	problem_berlin52 = tsplib95.load_problem('problems/berlin52.tsp')
	problem_berlin52.best_known = 7544.3659
	problem_berlin52.initial_path = utils.random_permutation([*range(1, problem_berlin52.dimension + 1, 1)])
	run_tests2(file_name="MAX_ITER_GREED_ACO_berlin52_sol" + "_{}".format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")), p=problem_berlin52)

	problem_kroA100 = tsplib95.load_problem('problems/kroA100.tsp')
	problem_kroA100.best_known = 21282.0
	problem_berlin52.initial_path = utils.random_permutation([*range(1, problem_kroA100.dimension + 1, 1)])
	run_tests2(file_name="MAX_ITER_GREED_kroA100_sol"+ "_{}".format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")), p=problem_kroA100)

