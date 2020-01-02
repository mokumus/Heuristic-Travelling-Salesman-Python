import aco
import csv
import tsplib95

def test_aco(file_name, problem, max_iters, num_ants, decay_amount, c_heur, c_local_pher, c_greed, number_of_runs=1):
	info = [0,float('inf'),0,0,float('inf')]
	file_path = "Table-Info/"
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
	test_aco(file_name, p, max_iters=75, num_ants=10, decay_amount=0.4, c_heur=3.0, c_local_pher=0.4, c_greed=1.0,number_of_runs=20)


def main():
	problem_berlin52 = tsplib95.load_problem('problems/berlin52.tsp')
	problem_berlin52.best_known = 7542
	#run_tests2(file_name="ACOLS__berlin52", p=problem_berlin52)

	problem_dantzig42 = tsplib95.load_problem('problems/dantzig42.tsp')
	problem_dantzig42.best_known = 699
	#run_tests2(file_name="ACOLS__dantzig42", p=problem_dantzig42)

	problem_eil51 = tsplib95.load_problem('problems/eil51.tsp')
	problem_eil51.best_known = 426
	#run_tests2(file_name="ACOLS__eil51", p=problem_eil51)

	problem_eil101 = tsplib95.load_problem('problems/eil101.tsp')
	problem_eil101.best_known = 629
	#run_tests2(file_name="ACOLS__eil101", p=problem_eil101)

	problem_pr107 = tsplib95.load_problem('problems/pr107.tsp')
	problem_pr107.best_known = 44303
	#run_tests2(file_name="ACOLS__pr107", p=problem_pr107)

	problem_ch130 = tsplib95.load_problem('problems/ch130.tsp')
	problem_ch130.best_known = 6110
	run_tests2(file_name="ACOLS__ch130", p=problem_ch130)

	problem_kroA200 = tsplib95.load_problem('problems/kroA200.tsp')
	problem_kroA200.best_known = 29368
	run_tests2(file_name="ACOLS__kroA200", p=problem_kroA200)

	problem_rat783 = tsplib95.load_problem('problems/rat783.tsp')
	problem_rat783.best_known = 8806
	run_tests2(file_name="ACOLS__rat783", p=problem_rat783)


if __name__ == '__main__':
	main()
