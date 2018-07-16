import random

from file_decode import *


class Chromosome(list):
    gene_values = np.ravel([list(classprof_time[i]) for i in classprof_time])
    gene_range = range(-1, len(gene_values))

    def __init__(self):
        self.size = 2 * len(courses_list)
        self.prof_num_of_courses = {p: 0 for p in profs_list}
        self.num_of_hard_conflicts = 0
        self.num_of_soft_conflicts = 0
        lst = [-1] * self.size
        super().__init__(lst)
        for i in range(len(courses_list)):
            if not course_prof[courses_list[i]]:
                continue
            self[i] = self.find_skilled_prof(i)
            if course_value[courses_list[i]] > 2:
                self[i + self.size // 2] = self.find_time_for_prof(self.get_gene_prof(i))
        self.hard_constraints_violated()
        self.soft_constraints_violated()

    def find_skilled_prof(self, nth):
        prof = random.sample(course_prof[courses_list[nth]], 1)[0]
        return self.find_time_for_prof(prof)

    def find_time_for_prof(self, prof):
        indexes = [i for i in range(len(classprof_time.keys())) if list(
            classprof_time.keys())[i].split('-')[0] == prof]
        lst = []
        for i in indexes:
            for j in range(timeslots_num):
                if self.gene_values[i * timeslots_num + j] == 1:
                    lst.append(i * timeslots_num + j)
        if len(lst) <= 1:
            return -1
        return lst[random.randint(0, len(lst) - 1)] if random.uniform(0, 1) <= 0.75 else -1

    def get_gene_prof(self, nth):
        gene = self[nth]
        if gene != -1:
            x = gene // timeslots_num
            if x >= len(list(classprof_time.keys())):
                print(gene, x, len(list(classprof_time.keys())))
            return list(classprof_time.keys())[x].split('-')[0]

    def get_gene_class(self, nth):
        gene = self[nth]
        if gene != -1:
            x = gene // timeslots_num
            return list(classprof_time.keys())[x].split('-')[1]

    def is_gene_time_valid(self, nth):
        gene = self[nth]
        if gene != -1:
            return self.gene_values[gene] == 1
        return True

    def hard_constraints_violated(self):
        self.num_of_hard_conflicts = 0
        pt = {p: [] for p in profs_list}
        ct = {c: [] for c in classes_list}
        for i in range(self.size):
            if self[i] != -1:
                pt[self.get_gene_prof(i)].append(self[i] % timeslots_num)
                ct[self.get_gene_class(i)].append(self[i] % timeslots_num)
            if i < self.size / 2:
                if course_value[courses_list[i]] <= 2 and self[i + self.size // 2] != -1 and self[i] != -1:
                    self.num_of_hard_conflicts += 1
                if course_value[courses_list[i]] > 2 and (self[i + self.size // 2] == -1 ^ self[i] == -1):
                    self.num_of_soft_conflicts += 1
                if self[i + self.size // 2] != -1 and self[i] != -1:
                    if self.get_gene_prof(i) != self.get_gene_prof(i + int(self.size / 2)):
                        self.num_of_hard_conflicts += 1
                    if self[i] % timeslots_num == self[i + self.size // 2] % timeslots_num:
                        self.num_of_hard_conflicts += 1
            if self[i] != -1 and self.get_gene_prof(i) not in course_prof[
                    courses_list[i if i < self.size / 2 else i - self.size // 2]]:
                self.num_of_hard_conflicts += 1
            if self[i] != -1 and courses_list[i if i < self.size / 2 else i - self.size // 2] in \
                    registers_more_than_20 and int(self.get_gene_class(i)) not in capacity_more_than_20:
                self.num_of_hard_conflicts += 1
            if self[i] != -1 and not self.is_gene_time_valid(i):
                self.num_of_hard_conflicts += 1
        for x in pt:
            self.num_of_hard_conflicts += (len(pt[x]) - len(set(pt[x])))
        for x in ct:
            self.num_of_hard_conflicts += (len(ct[x]) - len(set(ct[x])))

    def soft_constraints_violated(self):
        self.num_of_soft_conflicts = 0
        pc = {p: 0 for p in profs_list}
        tt = {t: [] for t in term_course.keys()}
        for i in range(self.size):
            if self[i] != -1:
                pc[self.get_gene_prof(i)] += 1
                if courses_list[i if i < self.size / 2 else i - self.size // 2] in course_term.keys():
                    tt[course_term[courses_list[i if i < self.size / 2 else i - self.size // 2]]].append(
                        self[i] % timeslots_num)
            if i < self.size / 2:
                if self[i + self.size // 2] != -1 and self[i] != -1 and \
                        self.get_gene_class(i) != self.get_gene_class(i + int(self.size / 2)):
                    self.num_of_soft_conflicts += 1
                if self[i] == -1 and self[i + self.size // 2] == -1:
                    self.num_of_soft_conflicts += 10
        for x in tt:
            self.num_of_soft_conflicts += (len(tt[x]) - len(set(tt[x])))
        for x in pc:
            self.num_of_soft_conflicts += (np.max(pc[x]) - np.min(pc[x]))

    def compute_fitness_value(self):
        return np.log(self.num_of_hard_conflicts * 10 + self.num_of_soft_conflicts)

    def mutate_chrm(self, r_m):
        mutated = False
        for r in range(self.size):
            if random.uniform(0, 1) <= r_m:
                if not course_prof[courses_list[r if r < self.size / 2 else r - self.size // 2]]:
                    continue
                self[r] = self.find_skilled_prof(r if r < self.size / 2 else r - self.size // 2)
                mutated = True
        return mutated
