#coding: utf-8
'''主调度函数'''

import logging
import pandas as pd
import itertools
import random

import conf
from network.agent_nn import AgentDeepNetwork
from system.system_simul import AHPSystemSimulator
from utils_global import *

# 配置日志输出
logging.basicConfig(level=10) #DEBUG level

# 先写核心小函数，然后按步骤进行做流程调度
## TODO: 架构组织，把一次调度只用一次的放在这，可能多次使用的放到util里面
def construct_comp_info():
    # 构造系统部件信息
    sys_comp_info = conf.SYSTEM_COMPONENT
    num_comp = len(sys_comp_info)
    sys_comp_info = add_use_embed_info(sys_comp_info)
    s_flatten_colname_list = [[]] * num_comp
    a_flatten_colname_list = [[]] * num_comp

    # 生成和组织列名
    for i in range(num_comp): #对每个component
        comp_info = sys_comp_info[i]
        comp_state_fc, comp_action_fc = feature_column_struct(comp_info)
        sys_comp_info[i]['comp_state_fc'] = comp_state_fc
        sys_comp_info[i]['comp_action_fc'] = comp_action_fc
        for j in range(len(comp_state_fc)): #对每个状态维度
            s_column_name = str(i) + '_' + str(j) + '_' + comp_state_fc[j]['feature_name']
            comp_state_fc[j]["flatten_column_name"] = s_column_name
            s_flatten_colname_list[i].append(s_column_name)
        for k in range(len(comp_action_fc)): #对每个行动维度
            a_column_name = str(i) + '_' + str(k) + '_' + comp_action_fc[k]['feature_name']
            comp_action_fc[k]["flatten_column_name"] = a_column_name
            a_flatten_colname_list[i].append(a_column_name)

    # 拉平成列表：系统全部列
    flatten_colname_list = [s_cn for comp_s_cn in s_flatten_colname_list for s_cn in comp_s_cn] + \
                            [a_cn for comp_a_cn in a_flatten_colname_list for a_cn in comp_a_cn]#CHECK: 顺序

    # 拉平成列表：按照agent分开组织
    agents = conf.AGENT_COMPONENTS
    comp_agent_mapping = revert_agent_comp_mapping(agents) # 构造倒排mapping
    num_agents = len(agents)
    s_flatten_colname_list_agent = [[]] * num_agents
    a_flatten_colname_list_agent = [[]] * num_agents
    for i in range(num_comp):
        comp_agent_index = comp_agent_mapping[str(i)]
        s_flatten_colname_list_agent[comp_agent_index].extend(s_flatten_colname_list[i])
        a_flatten_colname_list_agent[comp_agent_index].extend(a_flatten_colname_list[i])
    flatten_colname_list_agents = [[s_cn for s_cn in s_flatten_colname_list_agent[i]] + [a_cn for a_cn in a_flatten_colname_list_agent[i]] for i in range(num_agents)]
    return sys_comp_info, comp_agent_mapping, flatten_colname_list, flatten_colname_list_agents

# 按单个步骤进行实现，组织成类
class MaintainWorker:
    def __init__(self):
        self.current_sample_collection_org = []
        self.agents = conf.AGENT_COMPONENTS
        self.num_agents = len(self.agents)
        self.action_select_strategy = conf.ACTION_SELECT_STRATEGY
        self.action_select_params = conf.ACTION_SELECT_PARAMS
        self.agent_nn_batch_size = conf.BATCH_SIZE
        self.termination_criterion = conf.TERMINATION_CRITERION
        self.max_termination_num_iteration = conf.MAX_TERMINATION_NUM_ITERATION
        # 部件信息初始化
        self.sys_comp_info, self.comp_agent_mapping, self.flatten_colname_list, self.flatten_colname_list_agents = construct_comp_info()
        self.num_comp = len(self.sys_comp_info)
        self.length_of_comp_action = len(self.sys_comp_info[0]['comp_action_fc'])  # CHECK: 一个action的维度，应该是6
        # 历史样本存储和回放
        self.history_memory_df = pd.DataFrame(columns = self.flatten_colname_list.extend(['total_epoch', 'train_epoch']))
        self.replay_one_batch_size = conf.REPLAY_ONE_BATCH_SIZE
        self.replay_batch_num = conf.REPLAY_BATCH_NUM
        self.replay_after_epoch = conf.REPLAY_AFTER_EPOCH

    def initialization(self):
        '''全局初始化'''
        # 系统模块初始化
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

    def simulation(self, selected_action = None): #默认selected_action是None即不采取行动，用于initialization阶段自然转移
        '''系统采取action并进行仿真，直至遇到决策时间点，返回上次产生的成本，以及本次待干预的系统状态向量'''
        last_reward = self.system_simulator._progress_one_action(selected_action)
        system_states = self.system_simulator._progress_one_epoch()
        feasible_actions = self.system_simulator._update_feasible_action()
        return last_reward, system_states, feasible_actions

    def decision(self, system_states, feasible_actions):
        '''将系统状态传给神经网络作为样本，返回最优决策'''
        def gen_test_sample_agents(system_states, feasible_actions):
            # 将state和action按照agent分割
            agent_test_sample_state = []
            agent_feasible_actions = [[]] * self.num_agent
            for comp_index in range(self.num_comp):
                agent_test_sample_state[comp_index].append(system_states[comp_index])
                agent_index = self.comp_agent_mapping(str(comp_index))
                agent_feasible_actions[agent_index].append(feasible_actions[comp_index])

            agent_test_sample_actions = [[]] * self.num_agents
            agent_test_sample = [[]] * self.num_agents
            flatten_test_sample_agents_df_list = []
            for agent_index in range(self.num_agents):
                # 遍历形成所有可行的action样本
                feasible_actions_agent = agent_feasible_actions[agent_index]
                feasible_iter = [value_list for comp_value_list in feasible_actions_agent for value_list in comp_value_list]
                p_res = itertools.product(*feasible_iter)
                len_action = self.length_of_comp_action
                for s in p_res:
                    test_sample_action_org = [s[i: i+len_action] for i in range(0, len(s), len_action)] #CHECK: 是否有重叠
                    agent_test_sample_actions[agent_index].append(test_sample_action_org)

                # 将state和action进行拼接（都是organize格式）
                for action in agent_test_sample_actions[agent_index]:
                    agent_test_sample[agent_index].append([agent_test_sample_state[agent_index], action]) #在前面拼接state

                # 利用colname_agents转换成flatten格式的sample。可以直接复用sparse_flatten那个函数，需要额外传进一个对应的colname_list
                colname_list = self.flatten_colname_list_agents[agent_index]
                test_sample = agent_test_sample[agent_index]
                flattened_test_sample_df = sample_parse_flatten(test_sample, colname_list) #CHECK: 函数兼容性
                flatten_test_sample_agents_df_list.append(flattened_test_sample_df)

            return flatten_test_sample_agents_df_list

        flatten_test_sample_agents_df_list = gen_test_sample_agents(system_states, feasible_actions)
        # 对每个agent nn送入样本进行test
        pred_value = []
        agent_test_index = 0
        for an in self.agent_nns:
            pred_value.append(an._predict(flatten_test_sample_agents_df_list[agent_test_index]))
            agent_test_index += 1

        # 根据value选择每个agent的策略
        selected_action_dict = {}
        for agent_index in range(len(pred_value)):
            agent_best_action_index = select_best_action_agent(pred_value[agent_index], params = self.action_select_params, strategy = self.action_select_strategy)
            agent_best_action = agent_test_sample_actions[agent_index][agent_best_action_index]
            # 合并入dict结果
            agent_comps = self.agents[agent_index]
            for i in range(len(agent_comps)):
                comp_index = agent_comps[i]
                selected_action_dict[comp_index] = agent_best_action[i] #CHECK: 两个i是否对齐（正确的部件对应正确的行动）
        return selected_action_dict

    def sample_collect(self, system_states, selected_action_dict, reward):
        '''将系统产生的样本添加到当前样本集合中'''
        system_action_org = []
        for comp_index in range(self.num_comp):
            system_action_org.append(selected_action_dict[comp_index])
        self.current_sample_collection_org.append([system_states, system_action_org, reward])

    def memory_replay(self):
        '''从历史样本池中拿一部分连续样本返回'''
        replay_train_sample_df = pd.DataFrame(columns=self.flatten_colname_list.extend(['total_epoch', 'train_epoch']))
        current_memory_size = self.history_memory_df.shape[0]
        for i in range(self.replay_batch_num):
            index = random.randrange(0, current_memory_size)
            replay_batch_df = self.history_memory_df.iloc[index: min(index+self.replay_one_batch_size, current_memory_size), :] #CHECK:左右开闭情况
            replay_train_sample_df = pd.concat([replay_train_sample_df, replay_batch_df], axis=0)
        return replay_train_sample_df

    def network_train(self):
        '''样本凑够一个batch后，送入神经网络进行训练'''
        flatten_train_sample_df = sample_parse_flatten(self.current_sample_collection_org)
        # memory replay
        if self.total_epoch > self.replay_after_epoch:
            flatten_train_sample_df = pd.concat([flatten_train_sample_df, self.memory_replay()], axis=0)
        flatten_train_sample_agents_df_list = split_agent_flatten_sample(flatten_train_sample_df, self.flatten_colname_list, self.agents, self.comp_agent_mapping)
        agent_train_index = 0
        for an in self.agent_nns:
            an._train(flatten_train_sample_agents_df_list[agent_train_index])
            agent_train_index += 1
        flatten_train_sample_df['total_epoch'] = self.total_epoch
        flatten_train_sample_df['train_epoch'] = self.train_epoch
        self.history_memory_df = pd.concat([self.history_memory_df, flatten_train_sample_df], axis=0)

    def _go_to_work(self):
        #初始化
        self.initialization()

        #执行系统仿真、神经网络训练
        self.total_epoch = 0
        self.train_epoch = 0
        _, system_states, feasible_actions = self.simulation() #第一步冷启动
        while not is_terminate(self.total_epoch, self.termination_criterion, self.max_termination_num_iteration):
            self.total_epoch += 1 #第一步索引是epoch=1
            selected_action_dict = self.decision(system_states, feasible_actions)
            reward, system_states, feasible_actions = self.simulation(selected_action_dict)
            self.sample_collect(system_states, selected_action_dict, reward)
            if total_epoch % self.agent_nn_batch_size == 0:
                self.train_epoch += 1
                self.network_train()

    def _report_kpi(self):
        # TODO: 对关键指标做埋点，输出结果数值和指标
        return 0

    # TODO: 组织起来之后，继续做一些抽象，把高频功能函数集中到一起。目前能想到的是：如何组织system层面信息和agent层面信息，最好能有一个转换机制
    # TODO: 调试方法。先局部验证，然后进行关键结果做日志埋点，再调试。

if __name__ == "__main__":
    maintain_worker = MaintainWorker()
    maintain_worker._go_to_work()
    maintain_worker._report_kpi()
