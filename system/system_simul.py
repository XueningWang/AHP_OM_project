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
        self.num_comp = len(system_comp_info)
        # TODO:用这几个预留位置存储当前状态和行动
        self.current_action_best = []
        self.current_cost = []
        # 设定参数
        self.weibull_beta = conf.WEIBULL_BETA
        self.weibull_theta = conf.WEIBULL_THETA
        self.a_parm = conf.FAILURE_RATE_PARMS_a
        self.b_parm = conf.FAILURE_RATE_PARMS_b
        self.drainwater_lambda = conf.DRAINWATER_LAMBDA

    # 系统仿真相关
    # 功能1
    def init_system(self): #外部函数前面带下划线，"_func(xxx)"，内部私有函数不带，即"func(xxx)"
        '''对系统整体做初始化：部件状态归为完美状态等'''
        max_state = {'VL': conf.NUM_STATE_VALVE, 'NVL': conf.NUM_STATE_NONVALVE}
        init_failure_rate = 0
        init_bypath_vl_spare = 1
        # 仿真系统时间
        self.time = 0
        self.epoch = 0
        # 系统部件
        self.current_state = [[]] * self.num_comp
        for sc_info in self.system_comp_info:
            index = sc_info['index']
            vl_type = sc_info['valve_type']
            component_type = sc_info['component_type']
            initial_comp_state = [max_state[vl_type], init_failure_rate]
            if component_type == 'R':
                initial_comp_state.extend(init_bypath_vl_spare)
            self.current_state[index] = initial_comp_state
        # 部件上次维修和更换时间
        self.last_maintenance_time = [0] * self.num_comp
        self.last_replacement_time = [0] * self.num_comp
        # 部件下一个 time to failure
        self.ttf = [conf.INFINITE_TIME] * self.num_comp
        # 部件故障率分布参数：记录默认和累计的故障率放大和寿命提升参数
        self.default_failure_amplify = 1
        self.default_aging_reduction = 0
        self.acc_aging_a = [0] * self.num_comp
        self.acc_amplify_b = [1] * self.num_comp
        # 疏水产生过程
        self.num_heater = conf.NUM_HEATING_PATH * conf.HEATER_PER_HP
        self.drainwater_unit = conf.DRAINWATER_UNIT
        self.acc_drainwater = [0] * self.num_heater
        self.drainwater_next_tt_arival = [0] * self.num_heater
        self.drainwater_tta_list = []

    # 功能1：模拟系统内部的状态老化、状态依赖和条件响应过程
    def gen_deteriorate_ttf(self):
        comp_type = [sc_info['component_type'] for sc_info in self.system_comp_info]
        comp_beta = map(self.weibull_beta, comp_type)
        comp_theta = map(self.weibull_theta, comp_type)
        for ci in range(len(self.num_comp)):
            dist_parms = {'beta': comp_beta[ci], 'theta': comp_theta[ci], 'acc_a': self.acc_aging_a[ci],
                          'acc_b': self.acc_amplify_b[ci]}
            self.ttf[ci] = generate_random_lifetime(distribution='weibull', dist_args=dist_parms)
        return 0
    def gen_drainwater_ttf(self):
        if len(self.drainwater_tta_list) == 0:
            self.drainwater_tta_list = generate_random_lifetime(distribution='exp', dist_args={'lambda': self.drainwater_lambda}, type='batch', num=10000)
        for hi in range(len(self.num_heater)):
            self.drainwater_next_tt_arival[hi] = self.drainwater_tta_list.pop(0)

    def gen_drain_dependence(self):


        return 0

    def update_next_epoch(self):
        '''根据各部件寿命和维修活动，更新下一个系统转移的时间节点（预计最早的一个）'''
        # 产生接下来预计的状态转移时间
        self.gen_deteriorate_ttf()
        self.gen_drainwater_ttf()

        # 维修活动前，需要特殊处理且影响下一个决策时间点的：加热器状态（与自身故障率无关，由现存疏水量决定）

        # 维修活动前，需要特殊处理、但瞬时转移的：加热器水量过多->疏水阀打开；系统水量不足->旁路阀逐个打开
        def gen_drain_guard():
            return 0
        def gen_bypath_guard():
            return 0

        # 判断下一个决策时间点，组织好所有部件在该点的状态

    # 功能1
    def exec_action(self, action):
        '''拿到对每个部件的action之后，对系统部件做状态转移等一系列更新，计算成本'''
        # action是organized格式
        # 8.21更新：action是dict类型，即{comp_index : [comp_action]}

        # 维修活动后，需要更新状态的：新的故障率计算
        def update_failure_rate():
            return 0

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
