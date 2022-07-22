##MAIN

from jobshopproblem import *
from memetic_algorithm import *
import pandas as pd
from excel import *

if __name__ == '__main__':

    #name_instance = '10x10abz'

    #jobs = readFile('instancias/'+name_instance)

    #numMachines = len(jobs[0])
    #numJobs = len(jobs)
    instances = ['20x5ft20']
    size_populations = [10]
    iterations = [200]
    percent_preservs = [0.5]
    err_convergence = 0.0001
    iter_local_searchs = [10]

    for instance in instances:
        jobs = readFile('instancias/'+instance)
        numMachines = len(jobs[0])
        numJobs = len(jobs)
        print(instance)
        print("Cantidad de Maquinas:", numMachines)
        print("Cantidad de Trabajos:", numJobs)
        for i in range(11):
            for size_population in size_populations:
                for iteration in iterations:
                    for percent_preserv in percent_preservs:
                        for iter_local_search in iter_local_searchs:
                            print(size_population, iteration, percent_preserv, iter_local_search)
                            pop, exec_time = MA(size_pop=size_population, 
                                    iter=iteration, 
                                    preserv=percent_preserv, 
                                    e_conv=err_convergence, 
                                    iter_loc_search=iter_local_search, 
                                    jobs=jobs, 
                                    numjobs=numJobs, 
                                    nummachines=numMachines)
                            best_individual = best(pop)
                            result = pd.DataFrame({instance: [size_population, iteration, percent_preserv, err_convergence, iter_local_search, best_individual[0], exec_time]})
                            write_result(result, instance)

    #print("\n\nMejor Solución encontrada")    
    #print(best_individual)
    #print("Makespan: "+str(best_makespan))

