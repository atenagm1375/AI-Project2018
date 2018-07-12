import random

from file_decode import *


def find_skilled_prof(nth):
    prof = random.sample(course_prof[courses_list[nth]], 1)[0]
    cls = random.sample(classes_list, 1)[0]
    s = prof + '-' + str(cls)
    index = list(classprof_time.keys()).index(s)
    time = random.randint(0, timeslots_num - 1)
    return index * timeslots_num + time


class Chromosome(list):
    gene_values = np.ravel([list(classprof_time[i]) for i in classprof_time])
    gene_range = range(-1, len(gene_values))

    def __init__(self):
        self.size = 2 * len(courses_list)
        self.prof_num_of_courses = {p: 0 for p in profs_list}
        self.num_of_hard_conflicts = 0
        self.num_of_soft_conflicts = 0
        lst = [-1] * self.size
        for i in range(len(courses_list)):
            if not course_prof[courses_list[i]]:
                continue
            lst[i] = find_skilled_prof(i)
            if course_value[courses_list[i]] > 2:
                lst[i + self.size // 2] = find_skilled_prof(i)
        super().__init__(lst)
        for i in range(self.size):
            if self[i] != -1:
                self.gene_values[self[i]] -= 2
        self.hard_constraints_violated()
        self.soft_constraints_violated()

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
                    registers_more_than_20 and self.get_gene_class(i) not in capacity_more_than_20:
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
                    self.num_of_soft_conflicts += 1
        for x in tt:
            self.num_of_soft_conflicts += (len(tt[x]) - len(set(tt[x])))
        for x in pc:
            self.num_of_soft_conflicts += (np.max(pc[x]) - np.min(pc[x]))

    def compute_fitness_value(self):
        # return 2 - ((1 / (1 + 2 * self.num_of_hard_conflicts)) + (1 / (1 + self.num_of_soft_conflicts)))
        return 1 - (1 / (1 + np.sqrt(self.num_of_hard_conflicts) + np.sqrt(self.num_of_soft_conflicts)))

    def mutate_chrm(self, r_m):
        mutated = False
        for r in range(self.size):
            if random.uniform(0, 1) <= r_m:
                # rnd1 = random.randint(0, self.size - 1)
                # rnd2 = random.randint(0, self.size - 1)
                # if self[rnd1] != -1:
                #     self.gene_values[self[rnd1]] += 2
                # if self[rnd2] != -1:
                #     self.gene_values[self[rnd2]] += 2
                # ll = list(classprof_time.keys())
                # t1 = self[rnd1] % timeslots_num
                # t2 = self[rnd2] % timeslots_num
                # prof1 = ll[self[rnd1] // timeslots_num].split('-')[0]
                # prof2 = ll[self[rnd2] // timeslots_num].split('-')[0]
                # class1 = ll[self[rnd1] // timeslots_num].split('-')[1]
                # class2 = ll[self[rnd2] // timeslots_num].split('-')[1]
                # pc1 = prof1 + '-' + class2
                # pc2 = prof2 + '-' + class1
                # self[rnd1] = ll.index(pc1) * timeslots_num + t2
                # self[rnd2] = ll.index(pc2) * timeslots_num + t1
                # if self[rnd1] != -1:
                #     self.gene_values[self[rnd1]] -= 2
                # if self[rnd2] != -1:
                #     self.gene_values[self[rnd2]] -= 2
                if self[r] != -1 and self.gene_values[self[r]] < 0:
                    self.gene_values[self[r]] += 2
                self[r] = find_skilled_prof(r if r < self.size / 2 else r - self.size // 2)
                if self[r] != -1:
                    self.gene_values[self[r]] -= 2
                mutated = True
        return mutated

    def find_free_time_assist(self, nth, ind):
        ll = list(classprof_time.keys())
        val = ll.index(ind) * timeslots_num
        for i in range(timeslots_num):
            if self.gene_values[val + i] == 1:
                if self[nth] != -1 and self.gene_values[self[nth]] < 0:
                    self.gene_values[self[nth]] += 2
                self.gene_values[val + i] -= 2
                return val + i
        return -1

    def find_free_time(self, nth):
        t = -1
        ll = list(classprof_time.keys())
        prof = ll[self[nth] // timeslots_num].split('-')[0]
        cls = ll[self[nth] // timeslots_num].split('-')[1]
        if courses_list[nth if nth < self.size // 2 else nth - self.size // 2] in registers_more_than_20:
            if cls in capacity_more_than_20:
                t = self.find_free_time_assist(nth, prof + '-' + cls)
                if t != -1:
                    return t
            else:
                for c in capacity_more_than_20:
                    ind = prof + '-' + str(c)
                    t = self.find_free_time_assist(nth, ind)
                    if t != -1:
                        return t
        else:
            for c in classes_list:
                ind = prof + '-' + str(c)
                t = self.find_free_time_assist(nth, ind)
                if t != -1:
                    return t
        return t

    def repair(self):
        for i in range(self.size):
            if self[i] != -1:
                if i > self.size / 2 and self[i] != -1 \
                        and self.get_gene_prof(i) != self.get_gene_prof(i - self.size // 2):
                    ll = list(classprof_time.keys())
                    t2 = self[i - self.size // 2] % timeslots_num
                    prof1 = ll[self[i] // timeslots_num].split('-')[0]
                    class2 = ll[self[i - self.size // 2] // timeslots_num].split('-')[1]
                    pc1 = prof1 + '-' + class2
                    self[i] = ll.index(pc1) * timeslots_num + t2
                if self.gene_values[self[i]] < -1:
                    self[i] = self.find_free_time(i)