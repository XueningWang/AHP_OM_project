#coding: utf-8
'''主调度函数'''

import logging
import conf
from network.agent_nn import AgentDeepNetwork
from system.system_simul import AHPSystemSimulator
from utils_global import *

# 配置日志输出
logging.basicConfig(level=10) #DEBUG level

# 先写核心小函数，然后按步骤进行做流程调度
## TODO: 架构组织，把一次调度只用一次的放在这，可能多次使用的放到util里面
def construct_comp_info():
    sys_comp_info = conf.SYSTEM_COMPONENT
    sys_comp_info = add_use_embed_info(sys_comp_info)
    s_flatten_colname_list = []
    a_flatten_colname_list = []
    for i in range(len(sys_comp_info)):
        comp_info = sys_comp_info[i]
        comp_state_fc, comp_action_fc = feature_column_struct(comp_info)
        sys_comp_info[i]['comp_state_fc'] = comp_state_fc
        sys_comp_info[i]['comp_action_fc'] = comp_action_fc
        for j in range(len(comp_state_fc)):
            s_column_name = str(i) + '_' + str(j) + '_' + comp_state_fc[j]['feature_name']
            comp_state_fc[j]["flatten_column_name"] = s_column_name
            s_flatten_colname_list.append(s_column_name)
        for k in range(len(comp_action_fc)):
            a_column_name = str(i) + '_' + str(k) + '_' + comp_action_fc[k]['feature_name']
            comp_action_fc[k]["flatten_column_name"] = a_column_name
            a_flatten_colname_list.append(a_column_name)
    flatten_colname_list = s_flatten_colname_list + a_flatten_colname_list
    return sys_comp_info, flatten_colname_list

# 按单个步骤进行实现，组织成类
class MaintainWorker:
    def __init__(self):
        self.current_sample_collection_org = []
        self.agents = conf.AGENT_COMPONENTS

    #TODO: 8.13 重新组织下这些STEP
    def _initialize_step(self):
        '''全局初始化'''
        # 系统初始化
        self.sys_comp_info, self.flatten_colname_list = construct_comp_info()
        self.comp_agent_mapping = revert_agent_comp_mapping(self.agents)
        self.system_simulator = AHPSystemSimulator(self.sys_comp_info) #TODO:补充类初始化需要的参数
        self.system_simulator.system_init() #TODO:补充系统初始化函数需要的参数

        # 各AGENT的神经网络初始化
        agents = conf.AGENT_COMPONENTS
        num_agent = len(agents)
        self.agent_nns = []
        for agent_index in range(num_agent):
            agent_comp_info = []
            for comp_index in agents[agent_index]:
                agent_comp_info.append(sys_comp_info[comp_index])
            self.agent_nns.append(AgentDeepNetwork(agent_index, agents[agent_index], agent_comp_info))
            self.agent_nns[agent_index].network_init()

    def simulation(self, selected_action):
        '''系统采取action并进行仿真，直至遇到决策时间点，返回上次产生的成本，以及本次待干预的系统状态向量'''
        self.system_simulator._progress_one_action(selected_action)
        self.system_simulator._progress_one_epoch()
        test_sample = self.system_simulator._update_feasible_action()
        return test_sample

    def decision(self, test_sample):
        '''将系统状态传给神经网络作为样本，返回最优决策'''
        flatten_test_sample_df = sample_parse_flatten(test_sample)
        flatten_test_sample_agents_df_list = split_agent_flatten_sample(flatten_test_sample_df, self.flatten_colname_list, self.agents, self.comp_agent_mapping)
        # 对每个agent nn送入样本进行test
        pred_value = []
        agent_test_index = 0
        for an in self.agent_nns:
            pred_value.append(an._predict(flatten_test_sample_agents_df_list[agent_test_index]))
        # TODO: 8.21 需要着手考虑，预测结果是每个agent最好行为的情况下，如何将action拼在一起给到system；可能需要从生成预测样本时，就开始直接按照agent进行拆分，各自预测和转移。注意维护action与系统部件之间的映射关系

    def sample_collect(self):
        '''将系统产生的样本添加到当前样本集合中'''
        self.current_sample_collection_org.append(self.system_simulator._generate_one_sample())

    def memory_replay(self):
        '''从历史样本池中拿一部分样本返回'''
        # TODO: 8.13 写与文件打交道的处理

    def network_train(self):
        '''样本凑够一个batch后，送入神经网络进行训练'''
        flatten_train_sample_df = sample_parse_flatten(self.current_sample_collection_org)
        flatten_train_sample_agents_df_list = split_agent_flatten_sample(flatten_train_sample_df, self.flatten_colname_list, self.agents, self.comp_agent_mapping)
        # TODO: 8.13 把样本给到神经网络做预测（decision）/训练，先把原型写出来
