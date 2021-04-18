# -*- coding:utf-8 -*-
import Logger
from random import random

CPU_Speed = 2.5
CPU_Reduction = 2
CPU_Reduction_Rate = 0.8
F = 1.1089390193121363794595975343521e-40


class WorkStations(object):
    def __init__(self,
                 name: int,
                 load_capacity: int,  # CPU核数
                 capacity_constraints: float,  # 内存 在一个指定的区间内
                 status: bool = True,
                 frequency_ratio=1
                 ):
        self.name = name
        self.cpu_count = load_capacity
        self.load_capacity = load_capacity * CPU_Speed
        self.frequency_ratio = frequency_ratio
        self.capacity_constraints = capacity_constraints
        self.status = status
        self.time_consuming = 0  # 运行时间
        self.time_remaining = 0  # 当前任务运行剩余时间
        self.working = None  # 正在执行 [] / tasks
        self.queue = []  # 待执行队列
        self.logger = Logger.getLogger("WorkStation" + str(self.name))  # GetLogger
        self.complete_tasks = []
        self.current_all_time = 0

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
        self.current_all_time = time
        self.logger.info(
            "Next task:{},Time:{}".format([task.name for task in self.working].__str__(), self.time_remaining))

        # 判断是否需要降频
        self.judge_limit4(self.working)
        return 1  # 成功

    def judge_limit4(self, tasks: list):
        names = []
        for i in tasks:
            names.append(i.name)

        for task in tasks:
            total_work_load = 0
            for limits in task.limit4:
                if limits in names:
                    total_work_load += task.work_load
            if total_work_load > self.capacity_constraints * CPU_Reduction_Rate:
                self.load_capacity = CPU_Reduction * self.cpu_count  # 降频
                self.logger.debug(
                    "Cpu Reduced due to capacity of {} which on {}".format(total_work_load, self.capacity_constraints))
                break
        else:  # 不降频
            self.load_capacity = CPU_Speed * self.cpu_count

    def outage_possibility(self):
        sum_of_work_load = 0
        if not self.working:
            return 0
        for i in self.working:
            sum_of_work_load += i.work_load

        q = sum_of_work_load / self.load_capacity
        return F * (92 * q - 1)

    def time_passing(self, interval=1):
        if not self.status:
            return 0
        # 刷新宕机状态
        self.refresh_outage_status(interval)
        if not self.working:  # 判断是否正在工作
            self.start_next_task()  # 如果没在工作 尝试启动（用队列中的任务）这个情况是迁移任务的时候会出现的情况
            if not self.working:  # 再次判断
                return 0
        self.time_remaining -= interval
        if self.time_remaining <= interval:  # 粒度更小
            self.time_consuming += self.time_remaining
        else:
            self.time_consuming += interval
        self.logger.info("Time passed for {} seconds,Current task time left {}".format(interval, self.time_remaining))
        if self.time_remaining < 0:  # 这个任务结束了
            self.logger.info("Task finished:{},Current_Time:{}".format([task.name for task in self.working].__str__(),
                                                                       self.time_consuming))
            self.complete_tasks.append(self.current_all_time)  # 加入完成名单中
            self.start_next_task()

    def refresh_outage_status(self, interval=1):
        possibility = self.outage_possibility()
        self.logger.info("Random Possibility:{}".format(str(possibility)))
        if random() < possibility:
            # 宕机
            if random() < interval:
                # 考虑时间间隔
                self.logger.warning(
                    "WorkStation {} Stopped Working!(Outage),Current_task:{}".format(self.name, str(self.working)))
                self.status = False
                self.queue.append(self.working)
                self.time_remaining = 99999  # Infinity

    # TODO：服务器降频
