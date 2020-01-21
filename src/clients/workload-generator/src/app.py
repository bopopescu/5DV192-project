from WorkLoadGenerator import WorkLoadGenerator

if __name__ == '__main__':
    print("workload")
    workload_generator = WorkLoadGenerator()
    workload_generator.create_workload(5, 1)
    #workload_generator.worker_load("","","")