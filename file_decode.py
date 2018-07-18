import pandas as pd
import numpy as np

asked_class_dir = './files/AskedClass/'
capacity_dir = './files/capacity/'
chart_dir = './files/Chart/Chart.xlsx'
free_class_dir = './files/FreeClass/'
free_time_dir = './files/ProfFreeTime/'
skill_dir = './files/SKILL/'

skill_filenum, free_time_filenum, free_class_filenum, capacity_filenum, register_filenum, prof_num = 0, 0, 0, 2, 1, 10

skill_file = pd.read_excel(skill_dir + 'profskill' + str(skill_filenum) + '_profnumber-' + str(prof_num)
                           + '.xlsx', sheet_name=None)

del skill_dir

free_time_file = pd.read_excel(free_time_dir + 'prof_freetime' + str(free_time_filenum) + '_profnumber-' + str(prof_num)
                               + '.xlsx', sheet_name=None)

del free_time_dir

free_class_file = pd.read_excel(free_class_dir + 'Freeclass' + str(free_class_filenum) + '.xlsx', sheet_name=None)

del free_class_dir

chart_file = pd.read_excel(chart_dir, sheet_name=None)

del chart_dir

capacity_file = pd.read_excel(capacity_dir + 'class_capacity' + str(capacity_filenum) + '.xlsx', sheet_name=None)

del capacity_dir

asked_class_file = pd.read_excel(asked_class_dir + 'register' + str(register_filenum) + '.xlsx', sheet_name=None)

del asked_class_dir

skill_sheet1 = skill_file['Sheet1']

profs_list = list(skill_sheet1.index)

courses_list = list(skill_sheet1.keys())

course_value = {c: int(c.split('-')[1]) for c in courses_list}

course_prof = {i: [j for j in profs_list if skill_sheet1[i][j] == 1] for i in courses_list}

prof_course = {i: [j for j in courses_list if skill_sheet1[j][i] == 1] for i in profs_list}

del skill_file
del skill_sheet1

prof_time = {i: np.ravel(free_time_file[i]) for i in profs_list}

days = list(free_time_file[profs_list[0]].index)
times = list(free_time_file[profs_list[0]].columns)

timeslots_num = len(np.ravel(free_time_file[profs_list[0]]))

classes_list = list(free_class_file.keys())

class_time = {i: np.ravel(free_class_file[i]) for i in free_class_file.keys()}

classprof_time = {i + '-' + j: class_time[j] & prof_time[i] for i in profs_list for j in class_time.keys()}

del free_time_file
del free_class_file

chart_sheet1 = chart_file['Sheet1']

term_course = {c: list(chart_sheet1[c]) for c in chart_sheet1.keys()}

course_term = {list(chart_sheet1[c])[i]: c for c in chart_sheet1.keys() for i in range(len(list(chart_sheet1[c])))}

del chart_file
del chart_sheet1

capacity_sheet1 = capacity_file['Sheet1']

capacity_more_than_20 = [capacity_sheet1[capacity_sheet1.keys()[0]][i] for i in capacity_sheet1.index
                         if capacity_sheet1[capacity_sheet1.keys()[1]][i] == 0]

del capacity_file
del capacity_sheet1

registers_sheet1 = asked_class_file['Sheet1']

registers_more_than_20 = [registers_sheet1[registers_sheet1.keys()[0]][i] for i in registers_sheet1.index
                          if registers_sheet1[registers_sheet1.keys()[1]][i] == 0]

del asked_class_file
del registers_sheet1

prof_free_time_class = {p: [] for p in profs_list}
bin_values = np.ravel([list(classprof_time[i]) for i in classprof_time])
for i in range(len(classprof_time.keys())):
    for j in range(timeslots_num):
        if bin_values[i * timeslots_num + j] == 1:
            prof_free_time_class[list(classprof_time.keys())[i].split('-')[0]].append(i * timeslots_num + j)
