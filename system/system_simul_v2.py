'''系统仿真类实现（新）'''

import sys
sys.path.append('../')
import conf
from .utils_sys import *

class AHPSystemSimulator:
    def __init__(self, system_comp_info):
        '''初始化类：传入部件信息'''
        self.system_comp_info = system_comp_info  # 系统部件信息，来自main.py中的construct_comp_info()函数

    def init_system(self):
        '''初始化系统：系统归于完美状态；仿真时间归零；中间变量初始化'''
        # 部件配置初始化
        self.num_comp = len(self.system_comp_info)
        self.bypath_comp = conf.BYPATH_COMP
        # 设定参数
        self.initial_lambda = conf.INITIAL_LAMBDA
        self.failure_rate_parms_a = conf.FAILURE_RATE_PARMS_a
        self.failure_rate_parms_b = conf.FAILURE_RATE_PARMS_b
        # 仿真时间
        self.time = 0
        self.epoch = 0
        # 系统部件及当前状态
        self.current_failure_rate = [self.initial_lambda[cp['comp_type']] for cp in self.system_comp_info]  # 部件初始故障率赋值
        init_perfect_state = 0
        self.current_deter_state = [init_perfect_state for i in range(self.num_comp)] # 部件初始离散状态
        self.next_current_deter_state = self.current_deter_state + 1 # 默认下一个转移状态是当前的加1
        init_bypath_spare = 1
        self.current_bypath_spare = [init_bypath_spare for i in range(len(self.bypath_comp))]
        self.current_state = gen_comp_state(self.system_comp_info, self.bypath_comp, self.current_deter_state, self.current_failure_rate, self.current_bypath_spare)  # 生成部件初始状态
        # 部件上次维修和更换时间
        self.last_maintenance_time = [0] * self.num_comp
        self.last_replacement_time = [0] * self.num_comp
        self.last_transition_time = [0] * self.num_comp
        # 部件下一个 time to failure
        self.ttf = [conf.INFINITE_TIME] * self.num_comp
        # 旁路阀活跃情况
        self.num_bypath = conf.NUM_BY_PATH
        # 维修活动记录
        self.action_records_all = []
        self.current_epoch_cost = 0

        logging.info("Done system simulator init.")

    def gen_single_comp_ttf(self):
        '''整理单个部件的一次TTF（转移到下一个状态）'''
        comp_lambda = self.current_failure_rate
        for ci in range(self.num_comp):
            dist_parms = {'lambda': comp_lambda[ci]}
            self.ttf[ci] = generate_random_lifetime(distribution='exp', dist_args=dist_parms) #每次生成一个寿命分布
        return 0

    def gen_dependence_comps_ttf(self):
        # 加热器的加热部分、疏水部分、抽汽部分之间的联合转移仿真

        # 旁路阀与主干路之间的联合转移仿真（TODO: ？是否还考虑系统水量作为打开旁路阀的标准？会费时间计算系统指标）

    def update_next_epoch(self):
        '''根据各部件寿命和维修活动，更新下一个系统转移的时间节点（预计最早的一个）'''
        # 产生接下来预计的状态转移时间（先单个，再更新联合转移）
        self.gen_single_comp_ttf()
        self.gen_dependence_comps_ttf()
        # 判断下一个决策时间点，组织好所有部件在该点的状态
        tt_next_epoch = min(self.ttf)
        self.time = self.time + tt_next_epoch
        self.epoch += 1

    def cal_UGF(self):
        '''计算UGF（用于：排除UGF不满足阈值的解，或者将这些折成penalty）'''

    def gen_feasible_actions(self):
        '''生成可行的所有action组合，与state拼接后神经网络预测'''

    def update_failure_rate(self):
        '''用配置的故障率更新函数更新所有故障率'''
        for i in range(self.num_comp):
            self.current_failure_rate[i] = failure_augment_fn(self.current_failure_rate[i])

    def calc_cost(self, action_record):
        '''生成成本函数'''
        return cost_func(action_record)

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
        # 计算本次action造成的成本
        self.current_epoch_cost = self.calc_cost(record)
        # 补充一次action的time和epoch信息，将comp_record记录下来
        record["time"] = self.time
        record["epoch"] = self.epoch
        record["cost"] = self.current_epoch_cost
        self.action_records_all.append(record)

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
        return 0  # feasible_actions

    def _progress_one_action(self, selected_action):
        '''拿到神经网络的预测结果后，选择action并执行，求算出系统成本'''
        # 顺序调用以下函数: exec_action, calc_cost; 选择最佳策略的部分拿到main中做了
        reward = 0
        return reward

