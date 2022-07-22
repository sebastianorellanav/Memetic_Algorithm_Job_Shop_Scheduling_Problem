import matplotlib.pyplot as plt
from jobshopproblem import *
from memetic_algorithm import *
def MA_V2(size_pop=10, iter=100, preserv= 0.5, e_conv=0.0001, iter_loc_search=10, jobs=[], numjobs=0, nummachines=0):
    pop = []
    if jobs == []:
        return []
    a_i = []
    current_std = 0
    previous_std = 0
    makespans = []
    m = []
    generations = list(range(iter))

    #begin
    execution = time.time()
    pop = generate_initial_population(size_pop, jobs, numjobs, nummachines, iter_loc_search)
    while iter > 0: #agregar otra condición
        print("iteración n°: "+str(iter))
        pop = do_generation(pop, jobs, size_pop, iter_loc_search)
        fitness_best = makespan(jobs,best(pop, jobs))
        a_i.append(fitness_best)
        for p in pop:
            m.append(makespan(jobs, p))
        makespans.append(m)
        m = []
        current_std = np.std(a_i)
        if len(a_i) >=20 and (converged(current_std, previous_std, e_conv)):
            #print("restart population")
            a_i = []
            pop = restart_population(pop, jobs, numjobs, nummachines, preserv, iter_loc_search)
        previous_std = current_std
        iter-=1
    execution = time.time() - execution 
    plt.figure()
    plt.plot(generations,makespans, 'ro')
    plt.grid()
    #plt.legend(loc='best')
    plt.xlabel('Generación')
    plt.ylabel('Makespan (Fitness)')
    plt.title('Proceso de búsqueda algoritmo memético') 
    plt.show() 
    return pop, execution


instance = '10x10abz'
jobs = readFile('instancias/'+instance)
numMachines = len(jobs[0])
numJobs = len(jobs)
print(instance)
print("Cantidad de Maquinas:", numMachines)
print("Cantidad de Trabajos:", numJobs)


size_population = 10
iteration = 200
percent_preserv = 0.5
err_convergence = 0.0001
iter_local_search = 10
pop, exec_time = MA_V2(size_pop=size_population, 
                            iter=iteration, 
                            preserv=percent_preserv, 
                            e_conv=err_convergence, 
                            iter_loc_search=iter_local_search, 
                            jobs=jobs, 
                            numjobs=numJobs, 
                            nummachines=numMachines)