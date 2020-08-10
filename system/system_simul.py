#coding: utf-8
'''系统仿真类实现'''

sys.path.append('../')
import conf
from utils_sys import *

class AHPSystemSimulator:
    def __init__(self, system_comp_info):
        '''初始化类内部变量'''
        # 部件配置初始化
        self.system_comp_info = system_comp_info # 系统部件信息，来自main.py中的construct_comp_info()函数
        self.states = []  # 维护一个列表，每个元素是部件的状态。每个状态有2维，其中旁路阀的状态多了第3维
        self.ttf = []  # 维护一个列表，每个元素是一个部件在此时某状态上的寿命（由随机数生成），用于决定下一个系统决策时间点
        # 仿真过程初始化
        self.time = 0 #初始化时间为0
        #...

    # 系统仿真相关
    # 功能1
    def init_system(self): #外部函数前面带下划线，"_func(xxx)"，内部私有函数不带，即"func(xxx)"
        '''对系统整体做初始化：部件状态归为完美状态等'''

    # 功能1：参考仿真PPT
    def update_next_epoch(self):
        '''根据各部件寿命和维修活动，更新下一个系统转移的时间节点（预计最早的一个）'''
        # 调用utils_sys.py中的generate_random_lifetime生成一组或多组寿命分布

    # 功能1
    def exec_action(self, action):
        '''拿到对每个部件的action之后，对系统部件做状态转移等一系列更新，计算成本'''
        # action是organized格式

    # 功能1
    def calc_cost(self):
        '''用conf里的参数配置写好成本计算函数，计算一次维修活动的成本'''

    # 功能1
    def calc_system_performance(self):
        '''由系统各部件状态计算系统水量、加热效率这两个指标'''

    # 功能2
    # 输入与输出样本数据、与神经网络沟通相关
    def update_feasible_action(self): #wxn
        '''拿到一个决策时间点的系统状态后，将可行的action遍历，与状态拼成多个待预测的测试集样本'''
        # 调用util_global中的sample_parse_flatten()函数，将orgainized的格式转化成flatten的格式输出

    # 功能2
    def calc_best_action(self): #wxn
        '''拿到各测试集样本的近似Q value（即神经网络预测结果）后，根据value在各种action中选择一个action'''
        # 返回的action是orgainzed格式

    # 对外接口
    # 功能2
    def _progress_one_epoch(self):
        '''产出每个决策时间点，将可行action与系统状态拼接后返回'''
        # 顺序调用以下函数：update_next_epoch, update_feasible_action

    # 功能1
    def _progress_one_action(self):
        '''拿到神经网络的预测结果后，选择action并执行，求算出系统成本'''
        # 顺序调用以下函数：calc_best_action, exec_action, calc_cost

    # 功能3
    def _generate_one_sample(self): #wxn
        '''根据一个系统状态、一次施加的行动以及拿到的成本，变成一条结构化的数据（比如list或dict）'''
        # 将每一步exec_action时所用的那个最好的action，和本次的系统状态、cost放到一起，将数据格式由organized格式处理成flatten格式输出
