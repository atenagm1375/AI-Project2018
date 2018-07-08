import random
import sys

import numpy as np

from file_decode import classprof_time, profs_list, courses_list, course_value


class Chromosome(list):
    gene_values = np.ravel([list(classprof_time[i]) for i in classprof_time])
    gene_range = range(-1, len(gene_values))

    def __init__(self):
        self.size = 2 * len(courses_list)
        self.prof_num_of_courses = {p: 0 for p in profs_list}
        self.num_of_conflicts = 0
        self.fitness_value = sys.maxsize
        while True:
            rnd = random.sample(self.gene_range, self.size)
            if len(rnd) == len(set(rnd)):
                break
        for i in range(len(courses_list)):
            if course_value[courses_list[i]] <= 2:
                rnd[i + len(courses_list)] = -1
        super().__init__(rnd)
