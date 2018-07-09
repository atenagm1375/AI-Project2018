import collections
import difflib

from Chromosome import Chromosome


class Population(list):
    def __init__(self, length=0):
        super().__init__()
        for i in range(length):
            self.append(Chromosome())

    def fit(self):
        for p in self:
            p.hard_constraints_violated()
            p.soft_constraints_violated()

    def resolve_repeated(self, r_m):
        for i in range(len(self) - 1):
            if collections.Counter(self[i]) == collections.Counter(self[i + 1]):
                self[i].mutate_chrm(r_m)

    def is_mundane(self):
        for i in range(len(self) - 1):
            sm = difflib.SequenceMatcher(None, self[i], self[i + 1])
            if sm.ratio() < 0.9:
                return False
        return True
