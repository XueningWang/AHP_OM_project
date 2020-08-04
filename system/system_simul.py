#coding: utf-8
'''系统仿真类实现'''

from utils_sys import *

class AHPSystemSimulator:
    def __init__(self, conf):
        '''根据conf中配置的system系列参数，conf就是conf.py里面的字段'''
        self.system_params = conf.SYSTEM_PARAMS
        self.time = 0 #初始化时间为0
        self.states = [] #维护一个列表，每个元素是部件的状态
        self.ttf = [] #维护一个列表（或二维数组），每个元素是一个部件在某个状态上的一次寿命
        #...

    def system_init(self): #外部函数前面带下划线，"_func(xxx)"，内部私有函数不带，即"func(xxx)"
        '''对系统整体做初始化：部件状态归为完美状态等'''

    def update_next_epoch(self):
        '''根据各部件寿命和维修活动，更新下一个系统转移的时间节点（预计最早的一个）'''

    def calc_cost(self):
        '''用conf里的参数配置写好成本计算函数，计算一次维修活动的成本'''

    def conduct_action(self):
        '''拿到对每个部件的action之后，对系统部件做状态转移等一系列更新，计算成本'''

    def _generate_nn_sample(self):
        '''根据一个系统状态、一次施加的行动以及拿到的成本，变成一条结构化的数据（比如list或dict）'''
