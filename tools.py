# -*- coding:utf-8 -*-
import Logger
from Tasks import *


# 获取输入
def input_information():
    logger = Logger.getLogger("Tool")  # GetLogger
    # 记得初始化name为下标
    return [], []


'''
1. 部分任务不能分发到指定的工作站上；
2. 部分任务一定要同时运行在同一台工作站上；
3. 部分任务一定不能同时运行在同一台工作站上；
'''


def initial_deploy(workstation_list: list, tasks_list: list):
    logger = Logger.getLogger("Tool")  # GetLogger
    logger.info("Starting initial deployment...")
    for i in tasks_list:
        #TODO:并行任务此处还可以优化
        task_list = [i.name]
        work_load = i.work_load
        for other_tasks in i.limit2:
            work_load += tasks_list[other_tasks].work_load  # 并行
            task_list.append(other_tasks.name)
            tasks_list.pop(other_tasks.name) # 去重
        logger.debug("Work Load of {} task:{}".format(i.name, work_load))
        match_list = [0, 0]
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
            if match_rate > match_list[1]:  # 更新最新
                match_list[0] = j.name
                match_list[1] = match_rate
        # deploy
        workstation_list[match_list[0]].queue.append(task_list)
    return workstation_list


def calculate_balance(workstation_list: list):
    logger = Logger.getLogger("Tool")  # GetLogger
    logger.info("Start Calculating balance...")
    max_time = 0
    min_time = 0
    for i in workstation_list:
        if isinstance(i.working, list):  # 并行处理
            total_work_load = 0
            for task in i.working:
                total_work_load += task.work_load
        elif isinstance(i.working, Tasks):  # 串行处理
            total_work_load = i.working.work_load
        else:  # None
            logger.warning("workstation.working type unexpected!", i.working)
            total_work_load = 0

        for i_2 in i.queue:  # 加上队列中的时间
            total_work_load += i_2.work_load

        time = total_work_load / i.load_capacity
        if time > max_time:
            max_time = time
        if time < min_time:
            min_time = time
    logger.debug("balance ratio:", (max_time - min_time) / max_time)
    return (max_time - min_time) / max_time
