import vns
import csv
import tsplib95
from datetime import datetime

def test_vns(file_name, problem, number_of_runs = 1, n = 12, mni = 10, mnils = 65, pp=False, pes=False):
	info = [0,float('inf'),0,0,float('inf')]
	file_path = "results/"
	file_path +=file_name
	file_path += "_{}".format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p"))
	file_path += ".csv"
	with open(file_path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Time", "Initial Cost", "Minimized Cost", "Error Rate"])
		for i in range(0, number_of_runs):
			_ , csv_str = vns.search(problem, neighborhoods=n, max_no_improv=mni, max_no_improv_ls=mnils, plot_progress=pp, plot_end_start=pes)
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
	test_vns(file_name=file_name, number_of_runs=20, mni=10, mnils=20, pp=False, pes=False, problem=p)
	test_vns(file_name=file_name, number_of_runs=20, mni=10, mnils=40, pp=False, pes=False, problem=p)
	test_vns(file_name=file_name, number_of_runs=20, mni=10, mnils=60, pp=False, pes=False, problem=p)

	test_vns(file_name=file_name, number_of_runs=20, mni=10, mnils=20, pp=False, pes=False, problem=p)
	test_vns(file_name=file_name, number_of_runs=20, mni=20, mnils=20, pp=False, pes=False, problem=p)
	test_vns(file_name=file_name, number_of_runs=20, mni=40, mnils=20, pp=False, pes=False, problem=p)

	#Best scoring variables for berlin52, kroA100
	test_vns(file_name=file_name, number_of_runs=20, n=6, mni=40, mnils=20, pp=False, pes=False, problem=p)

	test_vns(file_name=file_name, number_of_runs=20, n=12, mni=40, mnils=30, pp=False, pes=False, problem=p)
	test_vns(file_name=file_name, number_of_runs=20, n=24, mni=40, mnils=40, pp=False, pes=False, problem=p)

	test_vns(file_name=file_name, number_of_runs=20, n=15, mni=40, mnils=20, pp=False, pes=False, problem=p)
	test_vns(file_name=file_name, number_of_runs=20, n=15, mni=40, mnils=30, pp=False, pes=False, problem=p)
	test_vns(file_name=file_name, number_of_runs=20, n=15, mni=40, mnils=40, pp=False, pes=False, problem=p)

if __name__ == '__main__':
	problem_berlin52 = tsplib95.load_problem('problems/berlin52.tsp')
	problem_berlin52.best_known = 7544.3659
	#run_tests(file_name="berlin52_sol", p=problem_berlin52)

	problem_kroA100 = tsplib95.load_problem('problems/kroA100.tsp')
	problem_kroA100.best_known = 21282.0
	#run_tests(file_name="kroA100_sol", p=problem_kroA100)