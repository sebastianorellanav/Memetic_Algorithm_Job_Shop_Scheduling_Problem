import random
from traceback import print_tb
from jobshopproblem import *

def select_from_population(pop, jobs):
    #rank based method
    makespans = []
    breeders = []
    for j in range(len(pop)):
        makespans.append((pop[j], makespan(jobs, pop[j])))
    
    pop_sorted = sorted(makespans, key=lambda schedule : schedule[1])

    for j in range(int(len(pop)/2)):
        breeders.append(pop_sorted[j][0])
    
    return breeders

def recombination(ind1, ind2, jobs):
    numJobs = len(jobs)
    numMachines = len(jobs[0])
    setJob1 = []
    setJob2 = []
    child1 = []
    child2 = []
    j = list(range(numJobs))
    while len(j) > 0:
        e = random.choice(j)
        j.remove(e)
        if len(setJob1) < 2:
            setJob1.append(e)
        else:
            setJob2.append(e)
    
    aux1 = setJob1*numMachines
    aux2 = setJob2*numMachines
    ### aqui ya tengo los job set ahora tengo que generar los hijos a partir de los padres
    for p1, p2, i in zip(ind1, ind2, range(len(ind1))):
        if p1 in setJob1:
            child1.append(p1)
        else:
            c = random.choice(aux2)
            aux2.remove(c)
            child1.append(c)
        
        if p2 in setJob2:
            child2.append(p2)
        else:
            c = random.choice(aux1)
            aux1.remove(c)
            child2.append(c)

    return child1, child2




def generate_new_population(breeders, jobs, size_pop):
    pop = []
    newpop = []
    
    # recombination
    i1 = -1
    i2 = -1
    for t in range(int(size_pop/2)):
        aux= breeders[:]
        parent1 = random.choice(aux)
        aux.remove(parent1)
        parent2 = random.choice(aux)
        child1, child2 = recombination(parent1, parent2, jobs)
        pop.append(child1)
        pop.append(child2)
    
    if len(pop) == size_pop+1:
        pop.pop()


    #mutation
    
    for j in range(len(pop)):
        newpop.append(local_improver(pop[j], jobs))
    
    return newpop


def update_population(pop, newpop, jobs):
    #plus replacement strategy
    makespans_pop = []
    makespans_newpop = []
    update_pop = []
    for j in range(len(pop)):
        makespans_pop.append((pop[j], makespan(jobs, pop[j])))
        makespans_newpop.append((newpop[j], makespan(jobs, newpop[j])))
    
    pop_sorted = sorted(makespans_pop, key=lambda schedule : schedule[1])
    newpop_sorted = sorted(makespans_newpop, key=lambda schedule : schedule[1])

    for j in range(int(len(pop)/2)):
        update_pop.append(pop_sorted[j][0])
        update_pop.append(newpop_sorted[j][0])

    return update_pop



#Listo
def apply_operator(ind, j):
    swapIndex = random.randrange(len(ind))
    ind[j], ind[swapIndex] = ind[swapIndex], ind[j]
    return ind

#Listo
def local_improver(current, jobs):
    for j in range(len(current)):
        new = apply_operator(current, j)
        
        
        if(makespan(jobs, new) < makespan(jobs, current)):
            current = new  
    
    return current

def best(pop, jobs):
    makespans = []
    for j in range(len(pop)):
        makespans.append((pop[j], makespan(jobs, pop[j])))
    
    pop_sorted = sorted(makespans, key=lambda schedule : schedule[1])

    return pop_sorted[0][0]

def converged(pop):
    return False


def do_generation(pop, jobs, size_pop):
    breeders = []
    newpop = []

    #begin
    
    breeders = select_from_population(pop, jobs)
    
    newpop = generate_new_population(breeders, jobs, size_pop)
    
    pop = update_population(pop, newpop, jobs)

    return pop


def generate_initial_population(size_pop, jobs, numjobs, nummachines):
    pop = []
    for j in range(size_pop):
        ind = generate_random_solution(numjobs, nummachines)
        pop.append(local_improver(ind, jobs))
    return pop

def restart_population(pop, jobs, numjobs, nummachines):
    newpop = []
    PRESERV = 0.5

    #begin
    preserved = len(pop)*PRESERV
    for j in range(int(preserved)):
        newpop.append(best(pop,jobs))
    
    for j in range(len(pop)-int(preserved)):
        ind = generate_random_solution(numjobs,nummachines)
        newpop.append(local_improver(ind, jobs))
    
    return newpop
    
def MA(size_pop=10, iter=100, jobs=[], numjobs=0, nummachines=0):
    pop = []
    if jobs == []:
        return []

    #begin
    pop = generate_initial_population(size_pop, jobs, numjobs, nummachines)
    while iter > 0:
        print("iteración n°: "+str(iter))
        pop = do_generation(pop, jobs, size_pop)
        if(converged(pop)):
            pop = restart_population(pop, jobs, numjobs, nummachines)

        iter-=1
        
    return pop
