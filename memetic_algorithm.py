from operator import le
import random
import numpy as np
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
        if len(setJob1) < numJobs/2:
            setJob1.append(e)
        else:
            setJob2.append(e)
    
    aux1 = setJob1*numMachines
    aux2 = setJob2*numMachines
    ### aqui ya tengo los job set ahora tengo que generar los hijos a partir de los padres
    for p1, p2 in zip(ind1, ind2):
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
def apply_operator(ind):
    j = random.randrange(len(ind))
    i = random.randrange(len(ind))
    while j == i:
        i = random.randrange(len(ind))

    if j > i:
        ind[i:j+1] = random.sample(ind[i:j+1], len(ind[i:j+1]))
    else:
        ind[j:i+1] = random.sample(ind[j:i+1], len(ind[j:i+1]))
    return ind

#Listo
def local_improver(current, jobs):
    iter = 40
    while iter > 0:
        new = apply_operator(current)
        if(makespan(jobs, new) < makespan(jobs, current)):
            current = new  
        iter -= 1
    return current

def best(pop, jobs):
    makespans = []
    for j in range(len(pop)):
        makespans.append((pop[j], makespan(jobs, pop[j])))
    
    pop_sorted = sorted(makespans, key=lambda schedule : schedule[1])

    return pop_sorted[0][0]

def converged(current_std, previous_std):
    error = 0.0001
    b_n = 1/2*(np.power((current_std - previous_std), 2))

    if b_n < error:
        return True

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
    a_i = []
    current_std = 0
    previous_std = 0
    #begin
    pop = generate_initial_population(size_pop, jobs, numjobs, nummachines)
    while iter > 0: #agregar otra condición
        print("iteración n°: "+str(iter))
        pop = do_generation(pop, jobs, size_pop)
        a_i.append(makespan(jobs,best(pop, jobs)))
        current_std = np.std(a_i)
        if len(a_i) >=20 and (converged(current_std, previous_std)):
            print("restart population")
            a_i = []
            pop = restart_population(pop, jobs, numjobs, nummachines)
        previous_std = current_std
        iter-=1
        
    return pop



