import random
import sys

from file_decode import *


class Chromosome(list):
    gene_values = np.ravel([list(classprof_time[i]) for i in classprof_time])
    gene_range = range(-1, len(gene_values))

    def __init__(self):
        self.size = 2 * len(courses_list)
        self.prof_num_of_courses = {p: 0 for p in profs_list}
        self.num_of_hard_conflicts = 0
        self.num_of_soft_conflicts = 0
        self.fitness_value = sys.maxsize
        while True:
            rnd = random.sample(self.gene_range, self.size)
            if len(rnd) == len(set(rnd)):
                break
        for i in range(len(courses_list)):
            if course_value[courses_list[i]] <= 2:
                rnd[i + len(courses_list)] = -1
        super().__init__(rnd)
        self.hard_constraints_violated()
        self.soft_constraints_violated()

    def get_gene_prof(self, nth):
        gene = self[nth]
        if gene != -1:
            time = gene % timeslots_num
            return list(classprof_time.keys())[time].split('-')[0]

    def get_gene_class(self, nth):
        gene = self[nth]
        if gene != -1:
            time = gene % timeslots_num
            return list(classprof_time.keys())[time].split('-')[1]

    def is_gene_time_valid(self, nth):
        gene = self[nth]
        if gene != -1:
            return self.gene_values[gene] == 1
        return True

    def hard_constraints_violated(self):
        pt = {p: [] for p in profs_list}
        ct = {c: [] for c in classes_list}
        for i in range(self.size):
            if self[i] != -1:
                pt[self.get_gene_prof(i)].append(self[i] % timeslots_num)
                ct[self.get_gene_class(i)].append(self[i] % timeslots_num)
            if i < self.size / 2:
                if course_value[courses_list[i]] <= 2 and self[i + int(self.size / 2)] != -1:
                    self.num_of_hard_conflicts += 10
                if self[i + int(self.size / 2)] != -1 and self[i] != -1:
                    if self.get_gene_prof(i) != self.get_gene_prof(i + int(self.size / 2)):
                        self.num_of_hard_conflicts += 4
                    if self[i] % timeslots_num == self[i + int(self.size / 2)] % timeslots_num:
                        self.num_of_hard_conflicts += 4
            if self[i] != -1 and self.gene_values[self[i]] == 0:
                self.num_of_hard_conflicts += 6
            if self[i] != -1 and self.get_gene_prof(i) not in course_prof[
                courses_list[i if i < self.size / 2 else i - int(self.size / 2)]]:
                self.num_of_hard_conflicts += 8
            if self[i] != -1 and courses_list[i if i < self.size / 2 else i - int(self.size / 2)] in \
                    registers_more_than_20 and self.get_gene_class(i) not in capacity_more_than_20:
                self.num_of_hard_conflicts += 2
        for x in pt:
            self.num_of_hard_conflicts += (2 * (len(pt[x]) - len(set(pt[x]))))
        for x in ct:
            self.num_of_hard_conflicts += (2 * (len(ct[x]) - len(set(ct[x]))))

    def soft_constraints_violated(self):
        pc = {p: 0 for p in profs_list}
        tt = {t: [] for t in term_course.keys()}
        for i in range(self.size):
            if self[i] != -1:
                pc[self.get_gene_prof(i)] += 1
                if courses_list[i if i < self.size / 2 else i - int(self.size / 2)] in course_term.keys():
                    tt[course_term[courses_list[i if i < self.size / 2 else i - int(self.size / 2)]]].append(
                        self.gene_values[self[i]])
            if i < self.size / 2:
                if self[i + int(self.size / 2)] != -1 and self[i] != -1 and \
                        self.get_gene_class(i) != self.get_gene_class(i + int(self.size / 2)):
                    self.num_of_soft_conflicts += 1
        for x in tt:
            self.num_of_soft_conflicts += (len(tt[x]) - len(set(tt[x])))
        for x in pc:
            self.num_of_soft_conflicts += (np.max(pc[x]) - np.min(pc[x]))

    def compute_fitness_value(self):
        return 2 - ((1 / (1 + self.num_of_hard_conflicts)) + (1 / (1 + np.arctan(self.num_of_soft_conflicts))))
