import threading
import time
from tools import *  # 记得去掉
import Logger

CPU_Speed = 2.1
CPU_Threshold = 1.9
CPU_Reduction = 1.8
Steal_Interval = 1

# TODO：note!使用线程锁

def workstation_working():
    logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    logger.info("Started!")
    current_time = 0
    while True:
        # TODO:等待偷取进行
        for workstation in workstation_list:
            workstation.time_passing()
        current_time += 1
        logger.debug("Current Time:", current_time)


def task_stealing():
    logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    logger.info("Started!")
    # Start Every second
    while True:



# Main thread
if __name__ == '__main__':
    # 启动线程
    main_logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    main_logger.debug(
        "Constant Definition:CPU_Speed = {},CPU_Threshold = {},CPU_Reduction = {}".format(CPU_Speed, CPU_Threshold,
                                                                                          CPU_Reduction))
    main_logger.info("Creating Child Threads...")
    WorkingThread = threading.Thread(target=workstation_working, name='WorkingThread')
    StealingThread = threading.Thread(target=task_stealing, name='StealingThread')
    main_logger.info("Child Threads Created Successfully!")

    main_logger.info("Reading Information...")
    tasks_list, workstation_list = input_information()
    main_logger.debug("Tasks:", tasks_list)
    main_logger.debug("Tasks Count:", len(tasks_list))
    main_logger.debug("WorkStations:", workstation_list)
    main_logger.debug("Tasks Count:", len(workstation_list))

    main_logger.info("Making Initial deployment...")
    # 更新工作站表
    workstation_list = initial_deploy(workstation_list, tasks_list)
    for i in workstation_list:
        i.start_next_task()
        main_logger.debug(i.name, i.queue)  # log:第一次部署的情况

    main_logger.info("Starting Child Threads...")
    WorkingThread.start()
    StealingThread.start()
