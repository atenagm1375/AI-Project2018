import random
from copy import deepcopy

from Chromosome import Chromosome
from Population import Population


def selection(pop):
    n = round(0.1 * number_of_population)
    new_pop = pop[:n]
    new_pop += random.sample(pop[n:], round(0.15 * number_of_population))
    new_pop.sort(key=Chromosome.compute_fitness_value)
    return new_pop


def crossover(pop, prob):
    children = Population()
    for first_par in pop:
        pop2 = deepcopy(pop)
        pop2.remove(first_par)
        for second_par in pop2:
            if random.uniform(0, 1) <= prob:
                points = random.sample(range(first_par.size), 2)
                child1 = deepcopy(first_par)
                child2 = deepcopy(second_par)
                child1[points[0]:points[1]], child2[points[0]:points[1]] = \
                    child2[points[0]:points[1]], child1[points[0]:points[1]]
                children.append(child1)
                children.append(child2)
    children.fit()
    children.sort(key=Chromosome.compute_fitness_value)
    return children


def mutation(pop, rate):
    children = Population()
    for p in deepcopy(pop):
        if p.mutate_chrm(rate):
            children.append(p)
    children.fit()
    return children


def replacement(pop, cross, mute):
    chld = cross + mute
    print(type(chld), type(cross), type(mute))
    chld.sort(key=Chromosome.compute_fitness_value)
    pop[round(0.1 * number_of_population):round(0.9 * number_of_population)] = chld[:round(0.8 * number_of_population)]
    return pop


number_of_population = 100
population = Population(number_of_population)
best = []

iteration = 0
while True:
    iteration += 1
    population.sort(key=Chromosome.compute_fitness_value)
    population.resolve_repeated(0.1)
    r_m = 0.05
    p_c = 0.8
    if len(best) < 10:
        best.append(population[0].compute_fitness_value())
    else:
        best[0] = population[0].compute_fitness_value()
    print(iteration, population[0].num_of_hard_conflicts, population[0].num_of_soft_conflicts, len(population))
    if population.is_mundane():
        break
    selected_population = selection(population)
    cross_children = crossover(selected_population, p_c)
    mut_children = mutation(cross_children, r_m)
    population = replacement(population, cross_children, mut_children)
