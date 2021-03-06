#coding: utf-8
'''系统仿真类实现'''

import sys
sys.path.append('../')
import conf
from .utils_sys import *

class AHPSystemSimulator:
    def __init__(self, system_comp_info):
        self.system_comp_info = system_comp_info  # 系统部件信息，来自main.py中的construct_comp_info()函数

    # 模块：初始化
    def init_system(self): #外部函数前面带下划线，"_func(xxx)"，内部私有函数不带，即"func(xxx)"
        '''系统初始化；仿真时间归零；中间变量初始化'''
        # 部件配置初始化
        self.num_comp = len(self.system_comp_info)
        self.current_action_best = []
        # 设定参数
        self.weibull_beta = conf.WEIBULL_BETA
        self.weibull_theta = conf.WEIBULL_THETA
        self.a_parm = conf.FAILURE_RATE_PARMS_a
        self.b_parm = conf.FAILURE_RATE_PARMS_b
        self.drainwater_lambda = conf.DRAINWATER_LAMBDA
        # 仿真时间
        self.time = 0
        self.epoch = 0
        # 系统部件
        self.current_state = [[]] * self.num_comp
        init_perfect_state = 0
        init_failure_rate = 0
        init_bypath_vl_spare = 1
        for sc_info in self.system_comp_info:
            index = sc_info['index']
            vl_type = sc_info['valve_type']
            comp_type = sc_info['comp_type']
            initial_comp_state = [init_perfect_state, init_failure_rate]
            if comp_type == 'R':
                initial_comp_state.append(init_bypath_vl_spare)
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
        self.drainwater_tta_list = [] # 多个疏水阀的疏水产生过程都由同一组参数决定，因此不分开生成
        # 疏水器和加热器对应关系
        heater_index = [i for i in range(self.num_comp) if self.system_comp_info[i]['comp_type'] == 'H']
        drain_index = [i for i in range(self.num_comp) if self.system_comp_info[i]['comp_type'] == 'K']
        self.heater_drain_match = dict(zip(heater_index, drain_index))
        self.heater_hindex = [{heater_index[j]: j} for j in range(len(heater_index))] # 表征某个加热器是第几个加热器的index
        # 疏水条件响应
        self.drainwater_guard_threshold = conf.DRAINWATER_GUARD_THRESHOLD

        # CHECK
        if self.num_heater != len(heater_index):
            print("FIX ME NOW. Unequal heater numbers! designed: %d, implemented: %d" %(self.num_heater, len(heater_index)))

        # 旁路阀活跃情况
        self.num_bypath = conf.NUM_BY_PATH
        self.perfect_sys_volume, self.perfect_sys_heating = self.calc_system_performance() # 完美情况下的系统表现
        self.sys_volume_guard_threshold = self.perfect_sys_volume * conf.SYS_VOLUME_THRESHOLD_RATIO
        self.sys_volume_unguard_threshold = self.perfect_sys_volume * conf.SYS_VOLUME_THRESHOLD_RATIO_UNGUARD
        self.current_active_NHP_valve = 0 # 初始情况下，没有一个旁路阀打开
        # 维修活动记录
        self.action_records = []
        self.current_epoch_cost = 0

        logging.info("Done system simulator init.")

    #模块：模拟系统内部的状态老化、状态依赖和条件响应过程
    def gen_deteriorate_ttf(self):
        comp_type = [sc_info['comp_type'] for sc_info in self.system_comp_info]
        comp_beta = map(self.weibull_beta, comp_type)
        comp_theta = map(self.weibull_theta, comp_type)
        for ci in range(len(self.num_comp)):
            dist_parms = {'beta': comp_beta[ci], 'theta': comp_theta[ci], 'acc_a': self.acc_aging_a[ci],
                          'acc_b': self.acc_amplify_b[ci]}
            self.ttf[ci] = generate_random_lifetime(distribution='weibull', dist_args=dist_parms)
        return 0
    def gen_drainwater_ttf(self):
        if len(self.drainwater_tta_list) <= self.num_heater:
            self.drainwater_tta_list.extend(generate_random_lifetime(distribution='exp', dist_args={'lambda': self.drainwater_lambda}, type='batch', num=10000))
        for hi in range(len(self.num_heater)):
            self.drainwater_next_tt_arival[hi] = self.drainwater_tta_list.pop(0)
    def gen_drain_dependence(self):
        self.gen_drainwater_ttf()
        for h,d in self.heater_drain_match.items():
            h_hindex = self.heater_hindex[h]
            self.ttf[h] = min(self.drainwater_next_tt_arival[h_hindex], self.ttf[d]) # 加热器下次转移的时间，是下次疏水阀转移和下次疏水产生二者中更近的那个
            h_state = self.acc_drainwater[h_hindex] + self.drainwater_unit - self.current_state[d][0] # 当前累积水量（上一时刻加热器疏水量）+一单位新产生疏水-疏水阀排水能力
            h_state = 0 if h_state < 0 else h_state #如果可以完全疏水，此时疏水量应为0
            self.current_state[h] = h_state
            self.acc_drainwater[h_hindex] = h_state

    def update_next_epoch(self):
        '''根据各部件寿命和维修活动，更新下一个系统转移的时间节点（预计最早的一个）'''
        # 产生接下来预计的状态转移时间
        self.gen_deteriorate_ttf()
        self.gen_drainwater_ttf()
        # 维修活动前，需要特殊处理且影响下一个决策时间点的：加热器状态（与自身故障率无关，由现存疏水量决定）
        self.gen_drain_dependence()
        # 判断下一个决策时间点，组织好所有部件在该点的状态
        tt_next_epoch = min(self.ttf)
        self.time = self.time + tt_next_epoch
        self.epoch += 1

    # 模块：执行维修活动
    # TODO: 10.6更新部件故障率
    def update_failure_rate(self):
        return 0
    # 疏水阀条件响应
    def gen_drain_guard(self):
        for h, d in self.heater_drain_match.items():
            if self.current_state[h][0] >= self.drainwater_guard_threshold:
                self.current_state[d][0] = 0 # 疏水阀立即变成完美状态
                #TODO: 10.6 条件响应是否产生cost或对故障率有所改变（有成本），还是只考虑成一个没有成本的自动过程？
        return 0
    # 旁路阀条件响应
    def gen_bypath_guard(self):
        # 每次响应只打开或关闭一个旁路阀，即使变动一个之后预计仍不满足要求，也不继续变动
        sys_volume, sys_heating = self.calc_system_performance()
        if sys_volume < self.sys_volume_guard_threshold and self.current_active_NHP_valve < self.num_bypath:
            # 系统水量过低且有阀可开，打开旁路阀
            self.current_active_NHP_valve += 1
            self.current_state[self.current_active_NHP_valve][2] = 0
        elif sys_volume >= self.sys_volume_unguard_threshold and self.current_active_NHP_valve > 0: # 系统水量恢复到安全水平，关闭旁路阀
            self.current_state[self.current_active_NHP_valve][2] = 1
            self.current_active_NHP_valve -= 1
        return 0

    def exec_action(self, action):
        '''拿到对每个部件的action之后，对系统部件做状态转移等一系列更新，计算成本'''
        record = {"OM": [], "OM_real_degree":[], "CBM": [], "CBM_real_degree":[], "RP":[]}
        # action是dict类型，即{comp_index : [comp_action]}
        # 根据传回的action执行维修活动
        for ci in range(self.num_comp):
            comp_action = action[ci] # [TH_om, TH_cbm, TH_re, U_om, U_cbm, RP, OM]
            # 更换
            if comp_action[5] == 1:
                self.current_state[ci][0], self.current_state[ci][1] = 0, 0
                record["RP"].append(ci)
            # 优先进行机会维修 TODO: 一个之前没有考虑到的点：需要保证只有机会出现时（其他部件在修），才进行机会维修
            elif comp_action[6] == 1:
                om_degree = min(self.current_state[ci][1], comp_action[3])
                self.current_state[ci][1] -= om_degree
                record["OM"].append(ci)
                record["OM_real_degree"].append(om_degree)
            # 视情维修
            elif comp_action[1] <= self.current_state[ci][1]:
                cbm_degree = min(self.current_state[ci][1], comp_action[4])
                self.current_state[ci][1] -= cbm_degree
                record["CBM"].append(ci)
                record["CBM_real_degree"].append(cbm_degree)

        # 维修活动后，需要更新状态的：新的故障率计算
        self.update_failure_rate()
        # 维修活动后，需要特殊处理的条件响应：加热器水量过多->疏水阀打开；系统水量不足->旁路阀逐个打开，系统水量回升至安全水平->旁路阀逐个关闭
        self.gen_drain_guard()
        self.gen_bypath_guard()
        # 计算本次action造成的成本
        self.current_epoch_cost = self.calc_cost()
        # 补充一次action的time和epoch信息，将comp_record记录下来
        record["time"] = self.time
        record["epoch"] = self.epoch
        record["cost"] = self.current_epoch_cost
        self.action_records.append(record)

    # 功能函数：成本计算
    def calc_cost(self):
        '''用conf里的参数配置写好成本计算函数，计算一次维修活动的成本'''
        # 成本应当包括：维修和更换成本、条件响应成本、系统水量水温的penalty
        return 0

    # 功能函数：计算系统表现指标 - 11.18 变成UGF的计算
    def calc_system_performance(self):
        '''由系统各部件状态计算系统水量、加热效率这两个指标'''
        sys_volume, sys_heating_efficiency = 0, 0
        return sys_volume, sys_heating_efficiency

    # 对外接口
    def _progress_one_epoch(self):
        '''产出每个决策时间点，将可行action与系统状态拼接后返回'''
        # 顺序调用以下函数：update_next_epoch
        # 应当返回system_states
        return 0

    def _update_feasible_action(self):  # wxn
        '''拿到一个决策时间点的系统状态后，将每个维度可行的action遍历'''
        # 返回值与system org action同形状，每个action位点上都是一个所有feasible的值的list
        # 注意辅助量的拼接。比如距上次维修时间、是否更换，都需要在这一步提供额外的信息
        return 0 #feasible_actions

    def _progress_one_action(self, selected_action):
        '''拿到神经网络的预测结果后，选择action并执行，求算出系统成本'''
        # 顺序调用以下函数: exec_action, calc_cost; 选择最佳策略的部分拿到main中做了
        reward = 0
        return reward
