import threading
import time
from tools import *  # 记得去掉
import Logger

logger = Logger.getLogger("Main")
logger.error("wtf")



def sever_working():
    for i in range(5):
        print(threading.current_thread().name + ' test ', i)
        time.sleep(1)


def task_stealing():
    pass


thread = threading.Thread(target=sever_working, name='TestThread')
thread.start()

for i in range(5):
    print(threading.current_thread().name + ' main ', i)
    time.sleep(1)
