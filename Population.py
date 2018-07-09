import collections

from Chromosome import Chromosome


class Population(list):
    def __init__(self, length=0):
        super().__init__()
        for i in range(length):
            self.append(Chromosome())

    def fit(self):
        f = []
        for p in self:
            p.compute_fitness_value()

    def resolve_repeated(self):
        for i in range(len(self) - 1):
            if collections.Counter(self[i]) == collections.Counter(self[i + 1]):
                self[i].mutate_chrm()
