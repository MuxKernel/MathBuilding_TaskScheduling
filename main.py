import threading
from time import sleep
from sys import exit
from tools import *  # 记得去掉
import Logger
import traceback
Steal_Interval = 0.01
Steal_Ratio = 0.7

lock = threading.Lock()  # 锁

def workstation_working():
    logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    logger.info("Started!")
    current_time = 0
    while True:
        lock.acquire()
        try:
            finished = True
            for workstation in workstation_list:
                workstation.time_passing(interval=Steal_Interval)
                if workstation.working:
                    finished = False
            current_time += Steal_Interval
            logger.debug("Current Time:" + str(current_time))
            if finished:
                logger.info("Finished All Tasks!")
                print_complete_map(workstation_list)
                sleep(10000)
        except Exception:
            logger.error("Sth happened...Something was Wrong!!!")
            traceback.print_exc()
        finally:
            lock.release()
            sleep(Steal_Interval/10)


def task_stealing():
    logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    logger.info("Started!")
    # Start Every Second
    while True:
        lock.acquire()
        try:
            previous_balance = 1
            while True:
                balance, max_workstation, min_workstation, outage = calculate_balance(workstation_list)
                if balance > previous_balance:  # 不平衡还高了
                    break
                if max_workstation == min_workstation:
                    logger.debug("Equal!Do not Steal!")
                    break
                if balance > Steal_Ratio:
                    steal_status = steal_tasks(workstation_list, max_workstation, min_workstation)
                    if not steal_status:  # 触底了
                        logger.warning("Cannot steal Tasks ...(All Tasks)")
                        # balance, max_workstation, min_workstation, outage = calculate_queue_balance(workstation_list)
                        # if balance > Steal_Ratio:
                        #     steal_status = steal_tasks(workstation_list, max_workstation, min_workstation)
                        #     if not steal_status:  # 时间最大的 再次触底了
                        if outage:  # 宕机就不管了
                            break
                        else:
                            logger.error("Cannot steal Tasks...Stealing Thread Exits(Only Queue)")
                            lock.release()
                            # 终止
                            sleep(10000)
                    else:  # 窃取成功
                        previous_balance = balance
            if outage:  # 去除宕机的
                logger.debug("Removing outage workstation...")
                workstation_list.pop(max_workstation)
        except ValueError:
            logger.error("Sth happened...Something was Wrong!!!")
        finally:
            lock.release()
            sleep(Steal_Interval / 10)


# Main thread
if __name__ == '__main__':
    # 启动线程
    main_logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    main_logger.info("Creating Child Threads...")
    WorkingThread = threading.Thread(target=workstation_working, name='WorkingThread')
    StealingThread = threading.Thread(target=task_stealing, name='StealingThread')
    main_logger.info("Child Threads Created Successfully!")

    main_logger.info("Reading Information...")
    workstation_list, tasks_list = input_information()
    main_logger.debug("Tasks Count:" + str(len(tasks_list)))
    main_logger.debug("WorkStations Count:" + str(len(workstation_list)))

    main_logger.info("Making Initial deployment...")
    # 更新工作站表
    workstation_list = initial_deploy(workstation_list, tasks_list)
    StealingThread.start()
    for i in workstation_list:
        log_info = ""
        for task_i in i.queue:
            log_info += " "
            for task_j in task_i:
                log_info += str(task_j.name)
                log_info += ","
        main_logger.debug("{}<-{}".format(i.name, log_info))  # log:第一次部署的情况
        i.start_next_task()

    main_logger.info("Starting Child Threads...")
    WorkingThread.start()
