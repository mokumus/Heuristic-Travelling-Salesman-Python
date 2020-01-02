import vns
import csv
import tsplib95

def test_vns(file_name, problem, number_of_runs = 20, n = 12, mni = 10, mnils = 65, pp=False, pes=False):
	info = [0,float('inf'),0,0,float('inf')]
	file_path = "Table-Info/"
	file_path +=file_name
	file_path += ".csv"
	with open(file_path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Time", "Initial Cost", "Minimized Cost", "Error Rate"])
		for i in range(0, number_of_runs):
			_ , csv_str = vns.vns_dynamic(problem, neighborhoods=n, max_no_improv=mni, max_no_improv_ls=mnils, plot_progress=pp, plot_end_start=pes)
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
		writer.writerow(["NEIGHBORHOODS   ", n])
		writer.writerow(["MAX_NO_IMPROV   ", mni])
		writer.writerow(["MAX_NO_IMPROV_LS", mnils])



def run_tests(file_name, p):
	#Best scoring variables for berlin52, kroA100
	test_vns(file_name=file_name, number_of_runs=20, n=6, mni=40, mnils=20, pp=False, pes=False, problem=p)

def main():
	problem_berlin52 = tsplib95.load_problem('problems/berlin52.tsp')
	problem_berlin52.best_known = 7542
	#run_tests(file_name="AVNS__berlin52", p=problem_berlin52)

	problem_dantzig42 = tsplib95.load_problem('problems/dantzig42.tsp')
	problem_dantzig42.best_known = 699
	#run_tests(file_name="AVNS__dantzig42", p=problem_dantzig42)

	problem_eil51 = tsplib95.load_problem('problems/eil51.tsp')
	problem_eil51.best_known = 426
	#run_tests(file_name="AVNS__eil51", p=problem_eil51)

	problem_eil101 = tsplib95.load_problem('problems/eil101.tsp')
	problem_eil101.best_known = 629
	#run_tests(file_name="AVNS__eil101", p=problem_eil101)

	problem_pr107 = tsplib95.load_problem('problems/pr107.tsp')
	problem_pr107.best_known = 44303
	run_tests(file_name="AVNS__pr107", p=problem_pr107)
'''
	problem_ch130 = tsplib95.load_problem('problems/ch130.tsp')
	problem_ch130.best_known = 6110
	run_tests(file_name="AVNS__ch130", p=problem_ch130)

	problem_kroA200 = tsplib95.load_problem('problems/kroA200.tsp')
	problem_kroA200.best_known = 29368
	run_tests(file_name="AVNS__kroA200", p=problem_kroA200)

	problem_rat783 = tsplib95.load_problem('problems/rat783.tsp')
	problem_rat783.best_known = 8806
	run_tests(file_name="AVNS__rat783", p=problem_rat783)

'''

if __name__ == '__main__':
	main()







