from Chromosome import Chromosome
from Population import Population

population = Population(100)
population.sort(key=Chromosome.compute_fitness_value)
print(population[0][0], population[4].get_gene_prof(0))
