# -*- coding:utf-8 -*-

from tools import *
import random
from copy import deepcopy as copy

def random_set(set: list,  lower: int,upper: int):
    # workstation_names
    count = random.randint(lower, upper)
    return random.sample(set, count)


workstation_list, tasks_list = input_information()
print(len(workstation_list))
for i in workstation_list:
    print(i.name, i.cpu_count, i.capacity_constraints)
workstation_names = list(range(len(workstation_list)))
tasks_names = list(range(len(tasks_list)))
del workstation_list  # 免得干扰打错变量

# limit 1
for i in tasks_list:
    limit_1 = random_set(workstation_names, 0, 4)
    if i.name in limit_1:
        i.limit1 = limit_1

# limit 2
for i in range(random.randint(80, 120)):
    limit_2 = random_set(tasks_names, 5, 10)
    for task in tasks_list:
        if task.name in limit_2:
            temp = copy(limit_2)
            temp.remove(task.name)
            task.limit2 = temp

# limit 3
for i in range(random.randint(20, 50)):
    limit_3 = random_set(tasks_names, 5, 12)
    for task in tasks_list:
        if task.name in limit_3:
            temp = copy(limit_3)
            temp.remove(task.name)
            task.limit3 = temp

# limit 4
for j in range(random.randint(7, 12)):
    limit_4 = random_set(tasks_names, 10, 40)
    for i in tasks_list:
        if i.name in limit_4:
            i.limit4 = limit_4

print(len(tasks_list))
for i in tasks_list:
    print(i.name, i.work_load, i.limit1, i.limit2, i.limit3, i.limit4)
