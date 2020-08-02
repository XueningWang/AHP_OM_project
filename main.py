#coding: utf-8

import logging
import conf
from network.agent_nn import AgentDeepNetwork
from system.system_simul import AHPSystemSimulator

# 配置日志输出
logging.basicConfig(level=10) #DEBUG level

# 按步骤实现核心逻辑
def initialize_step():
    '''全局初始化'''
    # 系统初始化
    system_simulator = AHPSystemSimulator() #TODO:补充类初始化需要的参数
    system_simulator.system_init() #TODO:补充系统初始化函数需要的参数

    # 各AGENT的神经网络初始化
    num_agent = len(conf.AGENT_COMPONENTS)
    agent_nns = []
    for agent_index in num_agent:
        agent_nns.append(AgentDeepNetwork(agent_index))
        agent_nns[agent_index].network_init()

def simulation_step(system_action):
    '''系统采取action并进行仿真，直至遇到决策时间点，返回上次产生的成本，以及本次待干预的系统状态向量'''

def decision_step():
    '''将系统状态传给神经网络作为样本，返回最优决策'''

def sample_collect_step():
    '''将一次的系统状态、采取的行动以及产生的成本记录下来'''

def network_training_step():
    '''样本凑够一个batch后，送入神经网络进行训练'''

