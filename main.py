#coding: utf-8
'''主调度函数'''

import logging
import conf
from network.agent_nn import AgentDeepNetwork
from system.system_simul import AHPSystemSimulator
from utils_global import *

# 配置日志输出
logging.basicConfig(level=10) #DEBUG level

# 按步骤实现核心逻辑
def initialize_step():
    '''全局初始化'''
    def construct_comp_info():
        sys_comp_info = conf.SYSTEM_COMPONENT
        sys_comp_info = add_use_embed_info(sys_comp_info)
        for i in range(len(sys_comp_info)):
            comp_info = sys_comp_info[i]
            comp_state_fc, comp_action_fc = feature_column_struct(comp_info)
            sys_comp_info[i]['comp_state_fc'] = comp_state_fc
            sys_comp_info[i]['comp_action_fc'] = comp_action_fc
        return sys_comp_info

    # 系统初始化
    sys_comp_info = construct_comp_info()
    system_simulator = AHPSystemSimulator(sys_comp_info) #TODO:补充类初始化需要的参数
    system_simulator.system_init() #TODO:补充系统初始化函数需要的参数

    # 各AGENT的神经网络初始化
    agents = conf.AGENT_COMPONENTS
    num_agent = len(agents)
    agent_nns = []
    for agent_index in range(num_agent):
        agent_comp_info = []
        for comp_index in agents[agent_index]:
            agent_comp_info.append(sys_comp_info[comp_index])
        agent_nns.append(AgentDeepNetwork(agent_index, agents[agent_index], agent_comp_info))
        agent_nns[agent_index].network_init()

def simulation_step(system_action):
    '''系统采取action并进行仿真，直至遇到决策时间点，返回上次产生的成本，以及本次待干预的系统状态向量'''

def decision_step():
    '''将系统状态传给神经网络作为样本，返回最优决策'''

def sample_collect_step():
    '''将一次的系统状态、采取的行动以及产生的成本记录下来'''

def network_training_step():
    '''样本凑够一个batch后，送入神经网络进行训练'''

