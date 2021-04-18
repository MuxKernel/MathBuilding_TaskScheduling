### 目录结构

- main.py：主程序入口，包含WorkingThread和StealingThread两个线程，运行main.py后复制粘贴数据集即可观察输出，最后程序运行完成之后会用sleep()阻塞两个线程，并输出每个工作站上对应的任务安排情况。
- Accumulation_histogram.py：可视化绘图（需要对程序输出数据进行特殊处理）
- Create_DataSet.py：在已有数据集的基础上随机添加四个限制条件
- Logger.py：附属模块，自定义的Colorful Logger方便调试
- Tasks.py：附属Tasks类
- WorkStations.py：附属WorkStations类，包括WorkStations自身的一些操作
- tools.py：主程序运行时的所有工具函数
- 数据集（全部包含100个WorkStations和1000个任务）：
  - Alibaba_cluster_with_all_limits.txt 使用阿里巴巴开源集群日志数据，随机添加限制条件
  - average.txt 服务器性能全部一致的数据集，Tasks使用阿里巴巴开源数据
  - average_with_all_limits.txt 同上，随机添加限制条件
  - average_with_limit_2.txt 同上，只添加第二个限制条件
  - large.txt 超大数据集，拥有1000个工作站和20000个任务，经测试，在以默认0.01秒为粒度运行时，算法解决时长是1分30秒，修改时间粒度为0.05秒后，算法解决时长是47秒。

### 使用方法

在pypy3.7-v7.3.3和cpython3.9上测试通过

运行main.py，复制数据集粘贴到控制台中

修改日志等级在Logger.py的51行中
修改时间粒度在main.py中的变量定义：Steal_Interval = 0.01
