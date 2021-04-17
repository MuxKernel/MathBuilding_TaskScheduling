# -*- coding:utf-8 -*-


class Tasks(object):
    def __init__(self,
                 name: int,
                 work_load: int,  # (内存)
                 limit1: list,  # 全部用序号表示
                 limit2: list,
                 limit3: list,
                 limit4: list, # 必须要包括自己
                 ):
        self.name = name
        self.work_load = work_load
        self.limit1 = limit1
        self.limit2 = limit2
        self.limit3 = limit3
        self.limit4 = limit4
