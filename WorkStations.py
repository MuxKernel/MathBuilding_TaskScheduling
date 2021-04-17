# -*- coding:utf-8 -*-
import Logger
from random import random

CPU_Speed = 2.5
CPU_Reduction = 2


class WorkStations(object):
    def __init__(self,
                 name: int,
                 load_capacity: int,  # CPU核数
                 capacity_constraints: int,  # 内存 在一个指定的区间内
                 status: bool = True,
                 frequency_ratio=1
                 ):
        self.name = name
        self.load_capacity = load_capacity * CPU_Speed
        self.frequency_ratio = frequency_ratio
        self.capacity_constraints = capacity_constraints
        self.status = status
        self.available_capacity = capacity_constraints  # 剩余内存
        self.time_consuming = 0  # 运行时间
        self.time_remaining = 0  # 当前任务运行剩余时间
        self.working = None  # 正在执行 [] / tasks
        self.queue = []  # 待执行队列
        self.logger = Logger.getLogger("WorkStation" + str(self.name))  # GetLogger

    def start_next_task(self):
        if not self.status:
            return 0
        if not self.queue:
            self.logger.info("Empty Queue,Cannot Start next task!")
            self.working = False
            self.time_remaining = 0
            return 0
        self.logger.debug("Trying to Start next task...")
        tasks = self.queue.pop(0)  # 底

        self.working = tasks
        time = 0
        for i in tasks:
            time += i.work_load / self.load_capacity
        self.time_remaining = time
        self.logger.info("Next task:{},Time:{}".format([task.name for task in self.working].__str__(), self.time_remaining))
        return 1  # 成功

    def time_passing(self, interval=1):
        if not self.status:
            return 0
        if not self.working:
            self.start_next_task()
            if not self.working: # 再次判断
                return 0
        self.time_remaining -= interval
        if self.time_remaining <= interval:  # 粒度更小
            self.time_consuming += self.time_remaining
        else:
            self.time_consuming += interval
        self.logger.info("Time passed for {} seconds,Current task time left {}".format(interval,self.time_remaining))
        if self.time_remaining < 0:  # 这个任务结束了
            self.logger.info("Task finished:{},Current_Time:{}".format([task.name for task in self.working].__str__(), self.time_consuming))
            self.start_next_task()

    def refresh_frequency_ratio(self):
        if not self.status:
            return 0
        pass

    def outage_possibility(self):
        return 0.95

    def refresh_outage_status(self):
        if random(0, 1) > self.outage_possibility():
            # 宕机
            self.status = False
            self.queue.append(self.working)
            self.time_remaining = 99999  # Infinity
            self.logger.warning(
                "WorkStation {} Stopped Working!(Outage),Current_task:{}".format(self.name, str(self.working)))

    #TODO：服务器降频