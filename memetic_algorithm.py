import random
import numpy as np
from jobshopproblem import *
import time

def select_from_population(pop):
    #rank based method
    breeders = []
    
    pop_sorted = sorted(pop, key=lambda schedule : schedule[0])

    for j in range(int(len(pop)/2)):
        breeders.append(pop_sorted[j])
    
    return breeders

def recombination(ind1, ind2, jobs):
    numJobs = len(jobs)
    setJob1 = []
    setJob2 = []
    child1 = []
    child2 = []
    j = random.sample(list(range(numJobs)),numJobs)
    setJob1 = j[:int(numJobs/2)]
    setJob2 = j[int(numJobs/2):]

    auxSetJob1 = setJob1.copy()
    auxSetJob1.append(auxSetJob1[0])
    auxSetJob1.pop(0)

    auxSetJob2 = setJob2.copy()
    auxSetJob2.append(auxSetJob2[0])
    auxSetJob2.pop(0)

    ### aqui ya tengo los job set ahora tengo que generar los hijos a partir de los padres
    for p1, p2 in zip(ind1, ind2):
        
        if p1 in setJob1:
            child1.append(p1)
        else:
            i = auxSetJob2.index(p1) 
            child1.append(setJob2[i]) 
        
        if p2 in setJob2:
            child2.append(p2)
        else:
            i = auxSetJob1.index(p2)
            child2.append(setJob1[i])

    return child1, child2




def generate_new_population(breeders, jobs, size_pop, iter_loc_search):
    pop = []
    newpop = []
    
    # recombination
    for t in range(int(size_pop/2)):
        aux= breeders.copy()
        parent1 = random.choice(aux)
        aux.remove(parent1)
        parent2 = random.choice(aux)
        child1, child2 = recombination(parent1[1], parent2[1], jobs)
        pop.append(child1)
        pop.append(child2)
    
    if len(pop) == size_pop+1:
        pop.pop()


    #mutation
    for agent in pop:
        agent_improved = local_improver(agent, jobs, iter_loc_search)
        newpop.append(agent_improved)
    
    return newpop

def getNeigbors(state, mode="random"):
    allNeighbors = []

    for i in range(len(state)-1):
        neighbor = state[:]
        if mode == "normal":
            swapIndex = i + 1
        elif mode == "random":
            swapIndex = random.randrange(len(state))
        neighbor[i], neighbor[swapIndex] = neighbor[swapIndex], neighbor[i]
        allNeighbors.append(neighbor)

    return allNeighbors

def update_population(pop, newpop):
    #plus replacement strategy
    update_pop = []

    pop_sorted = sorted(pop, key=lambda schedule : schedule[0])
    newpop_sorted = sorted(newpop, key=lambda schedule : schedule[0])
    for j in range(int(len(pop)/2)):
        update_pop.append(pop_sorted[j])
        update_pop.append(newpop_sorted[j])

    return update_pop

#Listo
def local_improver(current, jobs, iter):
    actualCost = makespan(jobs, current)
    newCost = 0
    while iter > 0:
        for new in getNeigbors(current):
            newCost = makespan(jobs, new)
            if(newCost < actualCost):
                current = new 
                actualCost = newCost 
        iter -= 1
            
    return (actualCost,current)

def best(pop): 
    pop_sorted = sorted(pop, key=lambda schedule : schedule[0])
    return pop_sorted[0]

def converged(current_std, previous_std, error):
    b_n = 1/2*(np.power((current_std - previous_std), 2))

    if b_n < error:
        return True

    return False



def do_generation(pop, jobs, size_pop, iter_loc_search):
    breeders = []
    newpop = []
    #begin
    breeders = select_from_population(pop)
    newpop = generate_new_population(breeders, jobs, size_pop, iter_loc_search) 
    pop = update_population(pop, newpop)

    return pop


def generate_initial_population(size_pop, jobs, numjobs, nummachines, iter_loc_search):
    pop = []
    for j in range(size_pop):
        ind = generate_random_solution(numjobs, nummachines)
        pop.append(local_improver(ind, jobs, iter_loc_search))
    return pop

def restart_population(pop, jobs, numjobs, nummachines, preserv, iter_loc_search):
    newpop = []
    #begin
    preserved = len(pop)*preserv
    for j in range(int(preserved)):
        newpop.append(best(pop))
    
    for j in range(len(pop)-int(preserved)):
        ind = generate_random_solution(numjobs,nummachines)
        newpop.append(local_improver(ind, jobs, iter_loc_search))
    
    return newpop
    
def MA(size_pop=10, iter=100, preserv= 0.5, e_conv=0.0001, iter_loc_search=10, jobs=[], numjobs=0, nummachines=0):
    pop = []
    if jobs == []:
        return []
    a_i = []
    current_std = 0
    previous_std = 0
    #begin
    aux = []
    execution = time.time()
    pop = generate_initial_population(size_pop, jobs, numjobs, nummachines, iter_loc_search)
    for m,agente in pop:
        aux.append((makespan(jobs, agente), agente))
        pop = aux
    while iter > 0: #agregar otra condición
        #print("iteración n°: "+str(iter))
        pop = do_generation(pop, jobs, size_pop, iter_loc_search)
        a_i.append(best(pop)[0])
        current_std = np.std(a_i)
        if len(a_i) >=20 and (converged(current_std, previous_std, e_conv)):
            a_i = []
            pop = restart_population(pop, jobs, numjobs, nummachines, preserv, iter_loc_search)
        previous_std = current_std
        iter-=1
    execution = time.time() - execution   
    return pop, execution


