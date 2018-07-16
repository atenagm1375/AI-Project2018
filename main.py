import math
import random
from copy import deepcopy

from generate_output import generate_output
from Chromosome import Chromosome, timeslots_num, course_value, courses_list
from Population import Population


def tournament_selection(pop, size=3):
    # print('selection')
    lst = []
    for i in range(size):
        lst.append(random.randint(0, size - 1))
    best = math.inf
    ans = pop[lst[0]]
    for i in lst:
        if pop[i].compute_fitness_value() < best:
            best = pop[i].compute_fitness_value()
            ans = pop[i]
    return ans


def crossover(pop, prob, swap=0.5):
    # print('crossover')
    children = Population()
    for x in range(number_of_population):
        parent1 = tournament_selection(pop)
        parent2 = tournament_selection(pop)
        child1 = deepcopy(parent1)
        if random.uniform(0, 1) <= prob:
            for i in range(child1.size):
                if random.uniform(0, 1) >= swap:
                    if child1[i] != parent2[i]:
                        child1[i] = parent2[i]
                    elif child1[i] != -1:
                        while True:
                            t1 = random.randint(0, timeslots_num - 1)
                            t2 = random.randint(0, timeslots_num - 1)
                            if t1 != t2:
                                break
                            child1[i] = child1[i] // timeslots_num + t1
        children.append(child1)
    return children


def mutation(pop, prob, rate=0.25):
    # print('mutation')
    for p in pop:
        for i in range(p.size // 2):
            if course_value[courses_list[i]] > 2:
                if p[i] == -1 ^ p[i + p.size // 2] == -1:
                    p[i] = p[i + p.size // 2] = -1
                elif p.get_gene_prof(i) != p.get_gene_prof(i + p.size // 2):
                    if random.uniform(0, 1) < 0.5:
                        p[i + p.size // 2] = p.find_time_for_prof(p.get_gene_prof(i))
                    else:
                        p[i] = p.find_time_for_prof(p.get_gene_prof(i + p.size // 2))

        if random.uniform(0, 1) <= prob:
            p.mutate_chrm(rate)


def main():
    global number_of_population
    number_of_population = 100
    print('initializing population...')
    population = Population(number_of_population)
    # best = []

    iteration = 0
    while True:
        number_of_population = len(population)
        iteration += 1
        population.sort(key=Chromosome.compute_fitness_value)
        p_r = 0.05
        p_c = 0.8
        print(iteration, population[0].num_of_hard_conflicts, population[0].num_of_soft_conflicts,
              population[0].compute_fitness_value())
        if population.is_mundane() or iteration == 1000:
            break
        children = crossover(population, p_c)
        mutation(children, p_r)
        children.fit()
        population = children
    generate_output(population[0])


main()
