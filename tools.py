# -*- coding:utf-8 -*-
import Logger
from Tasks import *
from WorkStations import *

"""
3
0 4 4
1 4 8
2 2 4
5
0 15 [1] [] [4] [0,1]
1 30 [] [] [] []
2 35 [] [] [] []
3 10 [] [4] [] []
4 8 [] [] [] []
"""


# 获取输入
def input_information():
    logger = Logger.getLogger("Tool")  # GetLogger
    # 记得初始化name为下标
    workstation_list = []
    tasks_list = []
    for i in range(int(input())):
        command = input().split(' ')  # 每一行的命令
        workstation = WorkStations(int(command[0]), int(command[1]), int(command[2]))
        workstation_list.append(workstation)
    del command
    for i in range(int(input())):
        command = input().split(' ')  # 每一行的命令
        task = Tasks(int(command[0]), int(command[1]), eval(command[2]), eval(command[3]), eval(command[4]),
                     eval(command[5]))
        tasks_list.append(task)
    return workstation_list, tasks_list


'''
1. 部分任务不能分发到指定的工作站上；
2. 部分任务一定要同时运行在同一台工作站上；
3. 部分任务一定不能同时运行在同一台工作站上；
'''


def initial_deploy(workstation_list: list, tasks_list: list):
    logger = Logger.getLogger("Tool")  # GetLogger
    logger.info("Starting initial deployment...")
    for i in tasks_list:
        # TODO:并行任务此处还可以优化
        task_list = [i]
        work_load = i.work_load
        for other_tasks in i.limit2:
            work_load += tasks_list[other_tasks].work_load  # 并行
            task_list.append(tasks_list[other_tasks])
            tasks_list.pop(other_tasks)  # 去重
        logger.debug("Total Work_Load of task {}:{}".format(i.name, str(work_load)))
        match_list = [-1, 0]
        for j in workstation_list:
            for banned_workstation in i.limit1:
                if j.name == banned_workstation:
                    logger.debug("Task {} Unable on Banned Workstation:{}".format(i.name, j.name))
                    continue
            for banned_task in i.limit3:
                if banned_task in j.queue:
                    logger.debug("Task {} Unable with Banned Task:{}".format(i.name, j.queue))
                    continue
            match_rate = work_load / j.capacity_constraints
            if match_rate > 1:  # 放不下
                continue # 换一个工作站
            if match_rate > match_list[1]:  # 更新最新
                match_list[0] = j.name
                match_list[1] = match_rate
        # deploy
        if match_list[0] == -1: # 没有一个能放下
            logger.error("No WorkStation can contain Task {}".format([task.name for task in task_list]))
        else:
            workstation_list[match_list[0]].queue.append(task_list)

    return workstation_list


def calculate_balance(workstation_list: list):
    logger = Logger.getLogger("Tool")  # GetLogger
    logger.info("Start Calculating balance...")
    max_time = [0, 0]
    min_time = [0, 0]
    outage = False
    for i in workstation_list:
        total_work_load = 0
        if not i.status:
            outage = True
        try:
            for task in i.working:
                total_work_load += task.work_load
        except TypeError:  # 如果为空
            pass
        try:
            for i_2 in i.queue:  # 加上队列中的时间
                for i_3 in i_2:
                    total_work_load += i_3.work_load
        except TypeError:  # 如果为空
            pass
        time = total_work_load / i.load_capacity
        if time > max_time[1]:
            max_time[0] = i.name
            max_time[1] = time
        if time <= min_time[1]:
            min_time[0] = i.name
            min_time[1] = time
    logger.debug("balance Output:ratio:" + str((max_time[1] - min_time[1]) / max_time[1]))
    logger.debug("balance Output:WorkStation:Max:{},Min:{}".format(max_time[0], min_time[0]))
    return (max_time[1] - min_time[1]) / max_time[1], max_time[0], min_time[0], outage


def steal_tasks(workstation_list: list, max_workstation: int, min_workstation: int):
    logger = Logger.getLogger("Tool")  # GetLogger
    try:
        task_max = workstation_list[max_workstation].queue.pop()
    except IndexError:
        logger.warning("{} Reached the bottom of Task Queue!".format(workstation_list[max_workstation].name))
        return 0
    logger.debug("Putting Task {} to WorkStation {}".format([task.name for task in task_max].__str__(),
                                                            workstation_list[min_workstation].name))
    workstation_list[min_workstation].queue.append(task_max)
    return 1


'''
def calculate_queue_balance(workstation_list: list):
    logger = Logger.getLogger("Tool")  # GetLogger
    logger.info("Start Calculating balance...")
    max_time = [0, 0]
    min_time = [0, 0]
    outage = False
    for i in workstation_list:
        if not i.status:
            outage = True
        if isinstance(i.working, list):  # 并行处理
            total_work_load = 0
            for task in i.working:
                total_work_load += task.work_load
        elif isinstance(i.working, Tasks):  # 串行处理
            total_work_load = i.working.work_load
        else:  # None
            logger.warning("workstation.working type unexpected!", i.working)
            total_work_load = 0
        time = total_work_load / i.load_capacity
        if time > max_time[1]:
            max_time[0] = i.name
            max_time[1] = time
        if time < min_time[1]:
            min_time[0] = i.name
            min_time[1] = time
    logger.debug("Queue balance Output:ratio:", (max_time[1] - min_time[1]) / max_time[1])
    logger.debug("Queue balance Output:WorkStation:Max:{},Min:{}".format(max_time[0], min_time[1]))
    return (max_time[1] - min_time[1]) / max_time[1], max_time[0], min_time[1],outage
'''


# TODO:把一些任务放在一起运行


def print_complete_map(workstation_list):
    logger = Logger.getLogger("Tool")  # GetLogger
    for i in workstation_list:
        log_info = ""
        for task_i in i.complete_tasks:
            log_info += " "
            for task_j in task_i:
                log_info += str(task_j.name)
                log_info += ","
        logger.debug("{}<-{}".format(i.name, log_info))  # log:完成情况
