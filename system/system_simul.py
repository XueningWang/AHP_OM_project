#coding: utf-8
'''系统仿真类实现'''

import sys
sys.path.append('../')
import conf
from .utils_sys import *

class AHPSystemSimulator:
    def __init__(self, system_comp_info):
        '''初始化类内部变量'''
        # 部件配置初始化
        self.system_comp_info = system_comp_info # 系统部件信息，来自main.py中的construct_comp_info()函数
        # TODO:用这几个预留位置存储当前状态和行动
        self.current_action_best = []
        self.current_cost = []
        # 设定参数
        self.weibull_beta = conf.WEIBULL_BETA
        self.weibull_theta = conf.WEIBULL_THETA
        self.a_parm = conf.FAILURE_RATE_PARMS_a
        self.b_parm = conf.FAILURE_RATE_PARMS_b

    # 系统仿真相关
    # 功能1
    def init_system(self): #外部函数前面带下划线，"_func(xxx)"，内部私有函数不带，即"func(xxx)"
        '''对系统整体做初始化：部件状态归为完美状态等'''
        num_comp = len(self.system_comp_info)
        max_state = {'VL': conf.NUM_STATE_VALVE, 'NVL': conf.NUM_STATE_NONVALVE}
        init_failure_rate = 0
        init_bypath_vl_spare = 1
        # 仿真系统时间
        self.time = 0
        self.epoch = 0
        # 系统部件
        self.current_state = [[]] * num_comp
        for sc_info in self.system_comp_info:
            index = sc_info['index']
            vl_type = sc_info['valve_type']
            component_type = sc_info['component_type']
            initial_comp_state = [max_state[vl_type], init_failure_rate]
            if component_type == 'R':
                initial_comp_state.extend(init_bypath_vl_spare)
            self.current_state[index] = initial_comp_state
        # 部件上次维修和更换时间
        self.last_maintenance_time = [0] * num_comp
        self.last_replacement_time = [0] * num_comp
        # 部件下一个 time to failure
        self.ttf = [conf.INFINITE_TIME] * num_comp

    # 功能1：参考仿真PPT
    def update_next_epoch(self):
        '''根据各部件寿命和维修活动，更新下一个系统转移的时间节点（预计最早的一个）'''
        # 调用utils_sys.py中的generate_random_lifetime生成一组或多组寿命分布
        def gen_deteriorate_ttf():

            return 0
        def gen_drain_dependence():
            return 0
        def gen_drain_guard():
            return 0
        def gen_bypath_guard():
            return 0
        def update_failure_rate():
            return 0

    # 功能1
    def exec_action(self, action):
        '''拿到对每个部件的action之后，对系统部件做状态转移等一系列更新，计算成本'''
        # action是organized格式
        # 8.21更新：action是dict类型，即{comp_index : [comp_action]}

    # 功能1
    def calc_cost(self):
        '''用conf里的参数配置写好成本计算函数，计算一次维修活动的成本'''

    # 功能1
    def calc_system_performance(self):
        '''由系统各部件状态计算系统水量、加热效率这两个指标'''

    # 对外接口
    # 功能2
    def _progress_one_epoch(self):
        '''产出每个决策时间点，将可行action与系统状态拼接后返回'''
        # 顺序调用以下函数：update_next_epoch
        # 应当返回system_states

    # 功能2
    # 输入与输出样本数据、与神经网络沟通相关
    def _update_feasible_action(self):  # wxn
        '''拿到一个决策时间点的系统状态后，将每个维度可行的action遍历'''

        # 返回值与system org action同形状，每个action位点上都是一个所有feasible的值的list
        feasible_actions = 0
        return feasible_actions

    # 功能1
    def _progress_one_action(self, selected_action):
        '''拿到神经网络的预测结果后，选择action并执行，求算出系统成本'''
        # 顺序调用以下函数: exec_action, calc_cost; 选择最佳策略的部分拿到main中做了
        reward = 0
        return reward
