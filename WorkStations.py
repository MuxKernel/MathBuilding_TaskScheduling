# -*- coding:utf-8 -*-
import Logger

CPU_Speed = 2.5
CPU_Reduction = 2


class WorkStations(object):
    def __init__(self,
                 name: int,
                 load_capacity: int,  # CPU速度
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
        self.logger.debug("Starting next task...")
        try:
            tasks = self.queue[0]  # 底
        except IndexError:  # 触底
            self.logger.warning("Reached the bottom of Task Queue!")
            return 0
        self.working = tasks
        time = 0
        for i in tasks:
            time += i.work_load / self.load_capacity
        self.time_remaining = time
        self.logger.info("Next task:{},Time:{}".format(str(self.working), self.time_remaining))
        return 1  # 成功

    def time_passing(self, interval=1):
        self.time_remaining -= interval
        if self.time_remaining < interval:  # 粒度更小
            self.time_consuming += self.time_remaining
        else:
            self.time_consuming += interval
        if self.time_remaining < 0:  # 这个任务结束了
            self.logger.info("Task finished:{},Current_Time:{}".format(str(self.working), self.time_consuming))
            self.start_next_task()
