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
    instances = ['10x10abz', '15x15la36', '20x5ft20', '20x15abz7']
    size_populations = [10, 20,30]
    iterations = [100,200,300]
    percent_preservs = [0.4,0.5,0.6]
    err_convergence = 0.0001
    iter_local_searchs = [10]

    for instance in instances:
        jobs = readFile('instancias/'+instance)
        numMachines = len(jobs[0])
        numJobs = len(jobs)
        print(instance)
        print("Cantidad de Maquinas:", numMachines)
        print("Cantidad de Trabajos:", numJobs)
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
                        best_individual = best(pop, jobs)
                        best_makespan = makespan(jobs, best_individual)
                        result = pd.DataFrame({instance: [size_population, iteration, percent_preserv, err_convergence, iter_local_search, best_makespan, exec_time]})
                        write_result(result, instance)

    #print("\n\nMejor Solución encontrada")    
    #print(best_individual)
    #print("Makespan: "+str(best_makespan))

