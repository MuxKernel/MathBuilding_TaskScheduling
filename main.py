import threading
import time
from tools import *  # 记得去掉
import Logger
# TODO：note!使用线程锁

def sever_working():
    logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    logger.info("Started!")


def task_stealing():
    logger = Logger.getLogger(threading.current_thread().name)  # GetLogger
    logger.info("Started!")


# Main thread
if __name__ == '__main__':
    # 启动线程
    WorkingThread = threading.Thread(target=sever_working, name='WorkingThread')
    StealingThread = threading.Thread(target=task_stealing, name='StealingThread')
    WorkingThread.start()
    StealingThread.start()



