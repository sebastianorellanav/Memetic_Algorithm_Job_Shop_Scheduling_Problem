##MAIN

from jobshopproblem import *
from memetic_algorithm import *

if __name__ == '__main__':
    jobs = readFile('instancias/10x10abz')

    numMachines = len(jobs[0])
    numJobs = len(jobs)
    print("Cantidad de Maquinas:", numMachines)
    print("Cantidad de Trabajos:", numJobs)
    printJobs(jobs)

    pop = MA(size_pop=20, iter=500, jobs=jobs, numjobs=numJobs, nummachines=numMachines)
    print("\n\nPoblación de soluciones encontradas")
    print(pop)
    print("\n\nMejor Solución encontrada")
    best_individual = best(pop, jobs)
    best_makespan = makespan(jobs, best_individual)
    print(best_individual)
    print("Makespan: "+str(best_makespan))

