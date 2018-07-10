import random
from copy import deepcopy

from Chromosome import Chromosome
from Population import Population


def selection(pop):
    # n = round(0.1 * number_of_population)
    ranked_prob = [1/(i + 1) for i in range(len(pop))]
    new_pop = random.choices(pop, weights=ranked_prob, k=round(0.2 * number_of_population))
    # new_pop = pop[:n]
    # new_pop += random.sample(pop[n:], round(0.15 * number_of_population))
    new_pop.sort(key=Chromosome.compute_fitness_value)
    return new_pop


# def crossover(pop, prob):
#     children = Population()
#     for first_par in range(len(pop)):
#         for second_par in range(first_par, len(pop)):
#             if random.uniform(0, 1) <= prob:
#                 points = random.sample(range(pop[first_par].size), 2)
#                 child1 = deepcopy(pop[first_par])
#                 child2 = deepcopy(pop[second_par])
#                 child1[points[0]:points[1]], child2[points[0]:points[1]] = \
#                     child2[points[0]:points[1]], child1[points[0]:points[1]]
#                 children.append(child1)
#                 children.append(child2)
#     children.fit()
#     children.sort(key=Chromosome.compute_fitness_value)
#     return children
def crossover(pop, prob):
    children = Population()
    while True:
        if len(children) == round(prob * number_of_population):
            break
        parents = random.sample(pop, 2)
        if random.uniform(0, 1) <= prob:
            points = random.sample(range(parents[0].size), 2)
            child1 = deepcopy(parents[0])
            child2 = deepcopy(parents[1])
            child1[points[0]:points[1]], child2[points[0]:points[1]] = \
                child2[points[0]:points[1]], child1[points[0]:points[1]]
            children.append(child1)
            children.append(child2)
    children.fit()
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
    chld.sort(key=Chromosome.compute_fitness_value)
    pop[round(0.2 * number_of_population):] = chld[:round(0.8 * number_of_population)]
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
    # for p in population:
    #     print(p.compute_fitness_value())
    if population.is_mundane():
        break
    selected_population = selection(population)
    cross_children = crossover(selected_population, p_c)
    mut_children = mutation(cross_children, r_m)
    population = replacement(population, cross_children, mut_children)
