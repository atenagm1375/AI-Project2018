import random
from copy import deepcopy

from Chromosome import Chromosome, timeslots_num
from Population import Population


def selection(pop):
    print('selection')
    ranked_pop = [1 / (i + 1) for i in range(len(pop))]
    new_pop = random.choices(pop, weights=ranked_pop, k=round(0.4 * number_of_population))
    return new_pop


def crossover(pop, prob, swap=0.5):
    print('crossover')
    children = Population()
    for x in range(len(pop)):
        for y in range(x, len(pop)):
            # parents = random.sample(pop, 2)
            # child1 = deepcopy(parents[0])
            # child2 = deepcopy(parents[1])
            child1 = deepcopy(pop[x])
            child2 = deepcopy(pop[y])
            if random.uniform(0, 1) <= prob:
                for i in range(child1.size):
                    if random.uniform(0, 1) >= swap:
                        if child1[i] != child2[i]:
                            child1[i], child2[i] = child2[i], child1[i]
                        elif child1[i] != -1:
                            while True:
                                t1 = random.randint(0, timeslots_num - 1)
                                t2 = random.randint(0, timeslots_num - 1)
                                if t1 != t2:
                                    break
                                child1[i] = child1[i] // timeslots_num + t1
                                child2[i] = child2[i] // timeslots_num + t2
            children.append(child1)
            children.append(child2)
    children.fit()
    return children


def mutation(pop, rate):
    print('mutation')
    children = Population()
    pop2 = deepcopy(pop)
    for p in pop2:
        if p.mutate_chrm(rate):
            children.append(p)
    children.fit()
    return children


def replacement(pop, cross, mute):
    print('replacement')
    chld = cross
    chld += mute
    chld.sort(key=Chromosome.compute_fitness_value)
    n = len(chld) - number_of_population
    # n = round(0.1 * number_of_population)
    # chld[len(chld) - n:] = pop[:n]
    # return chld
    # for i in range(n):
    #     chld.pop()
    pop[round(0.1 * number_of_population):] = chld[:round(0.9 * number_of_population)]
    return chld


def main():
    global number_of_population
    number_of_population = 100
    population = Population(number_of_population)
    # best = []

    iteration = 0
    while True:
        iteration += 1
        population.sort(key=Chromosome.compute_fitness_value)
        population.resolve_repeated(0.1)
        # for p in population:
        #     print(p.num_of_hard_conflicts, p.num_of_soft_conflicts)
        r_m = 0.05
        p_c = 0.8
        # if len(best) < 10:
        #     best.append(population[0].compute_fitness_value())
        # else:
        #     best[0] = population[0].compute_fitness_value()
        print(iteration, population[0].num_of_hard_conflicts, population[0].num_of_soft_conflicts, len(population))
        if population.is_mundane():
            break
        selected_population = selection(population)
        cross_children = crossover(selected_population, p_c)
        mut_children = mutation(cross_children, r_m)
        population = replacement(population, cross_children, mut_children)


main()
