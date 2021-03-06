#coding: utf-8
'''提供全局调度相关的子函数'''

import pandas as pd
import logging
import random
import json

import conf
from network.utils_net import *

# 用系统信息组织成特征信息，粒度是一个部件
def feature_column_struct(comp_info):
    comp_index = comp_info['index']
    comp_name = comp_info['name']
    comp_state_fc = [
            # 第一维，部件离散状态
            {"component_index": comp_index,
             "feature_name": comp_name+'_deterioration_state',
             "dtype": 'int',
             "method": categorical_int_method,
             "use_embedding": comp_info.get("state_use_embedding", False),
             "embed_vec_size": conf.STATE_DETER_EMBED_VECSIZE,
             "int_bucket_size": conf.STATE_DETER_BUCKET_SIZE,
             "network_usage": ['dense']
             },
            # 第二维，部件基础故障率
            {"component_index": comp_index,
             "feature_name": comp_name+'_failure_state',
             "dtype": 'double',
             "method": direct_numeric_method,
             "use_embedding": False,
             "network_usage": ['dense']
             }
        ]
    if comp_info['comp_type'] == "R":  # 疏水器单独加第三维特征，表示是否为备件状态
        comp_state_fc.append({"component_index": comp_index,
                              "feature_name": comp_name + '_isactive_state',
                              "dtype": 'int',
                              'method': categorical_binary_method,
                              "use_embedding": False,
                              "network_usage": ['dense']
                              })
    comp_action_fc = [
            # 第1维：机会维修阈值
            {"component_index": comp_index,
             "feature_name": comp_name + '_omth_action',
             "dtype": 'int',
             "method": categorical_int_method,
             "use_embedding": True,
             "embed_vec_size": conf.ACTION_DETER_EMBED_VECSIZE,
             "int_bucket_size": conf.STATE_DETER_BUCKET_SIZE,
             "network_usage": ['sparse']
             },
            # 第2维：视情维修阈值
            {"component_index": comp_index,
             "feature_name": comp_name + '_cbmth_action',
             "dtype": 'int',
             "method": categorical_int_method,
             "use_embedding": True,
             "embed_vec_size": conf.ACTION_DETER_EMBED_VECSIZE,
             "int_bucket_size": conf.STATE_DETER_BUCKET_SIZE,
             "network_usage": ['sparse']
             },
            # 第3维：更换阈值
            {"component_index": comp_index,
             "feature_name": comp_name + '_rpth_action',
             "dtype": 'double',
             "method": direct_numeric_method,
             "use_embedding": False,
             "network_usage": ['dense']
             },
            # 第4维：机会维修对部件状态提升水平
            {"component_index": comp_index,
             "feature_name": comp_name + '_omimp_action',
             "dtype": 'int',
             "method": categorical_int_method,
             "use_embedding": True,
             "embed_vec_size": conf.ACTION_DETER_EMBED_VECSIZE,
             "int_bucket_size": conf.STATE_DETER_BUCKET_SIZE,
             "network_usage": ['sparse']
             },
            # 第5维：视情维修对部件状态提升水平
            {"component_index": comp_index,
             "feature_name": comp_name + '_cbmimp_action',
             "dtype": 'int',
             "method": categorical_int_method,
             "use_embedding": True,
             "embed_vec_size": conf.ACTION_DETER_EMBED_VECSIZE,
             "int_bucket_size": conf.STATE_DETER_BUCKET_SIZE,
             "network_usage": ['sparse']
             },
            # 第6维：是否进行更换
            {"component_index": comp_index,
             "feature_name": comp_name + '_isreplece_action',
             "dtype": 'int',
             "method": categorical_binary_method,
             "use_embedding": True,
             "embed_vec_size": conf.ACTION_REPLACE_EMBED_VECSIZE,
             "network_usage": ['sparse']
             },
            # 第7维：是否进行机会维修
            {"component_index": comp_index,
             "feature_name": comp_name + '_isom_action',
             "dtype": 'int',
             "method": categorical_binary_method,
             "use_embedding": True,
             "embed_vec_size": conf.ACTION_OM_EMBED_VECSIZE,
             "network_usage": ['sparse']
            },
    ]
    return comp_state_fc, comp_action_fc

## TODO: 架构组织，把一次调度只用一次的放在这，可能多次使用的放到util里面
def construct_comp_info(sys_comp_info, agents):
    logging.info("Now constructing system components' info")

    # 构造系统部件信息
    num_comp = len(sys_comp_info)
    sys_comp_info = add_use_embed_info(sys_comp_info)
    s_flatten_colname_list = [[]] * num_comp
    a_flatten_colname_list = [[]] * num_comp

    # 生成和组织列名
    for i in range(num_comp): #对每个component
        comp_info = sys_comp_info[i]
        comp_state_fc, comp_action_fc = feature_column_struct(comp_info)
        for j in range(len(comp_state_fc)): #对每个状态维度
            s_column_name = str(i) + '_' + str(j) + '_' + comp_state_fc[j]['feature_name']
            comp_state_fc[j]["flatten_column_name"] = s_column_name
            s_flatten_colname_list[i].append(s_column_name)
        for k in range(len(comp_action_fc)): #对每个行动维度
            a_column_name = str(i) + '_' + str(k) + '_' + comp_action_fc[k]['feature_name']
            comp_action_fc[k]["flatten_column_name"] = a_column_name
            a_flatten_colname_list[i].append(a_column_name)
        sys_comp_info[i]['comp_state_fc'] = comp_state_fc
        sys_comp_info[i]['comp_action_fc'] = comp_action_fc

    # 拉平成列表：系统全部列
    flatten_colname_list = [s_cn for comp_s_cn in s_flatten_colname_list for s_cn in comp_s_cn] + \
                            [a_cn for comp_a_cn in a_flatten_colname_list for a_cn in comp_a_cn]#CHECK: 顺序

    # 拉平成列表：按照agent分开组织
    comp_agent_mapping = revert_agent_comp_mapping(agents) # 构造倒排mapping
    num_agents = len(agents)
    s_flatten_colname_list_agent = [[]] * num_agents
    a_flatten_colname_list_agent = [[]] * num_agents
    for i in range(num_comp):
        comp_agent_index = comp_agent_mapping[i]
        s_flatten_colname_list_agent[comp_agent_index].extend(s_flatten_colname_list[i])
        a_flatten_colname_list_agent[comp_agent_index].extend(a_flatten_colname_list[i])
    flatten_colname_list_agents = [[s_cn for s_cn in s_flatten_colname_list_agent[i]] + [a_cn for a_cn in a_flatten_colname_list_agent[i]] for i in range(num_agents)]

    # DEBUG
    # print("construct_comp_info preview - sys_comp_info")
    # for ci in sys_comp_info:
    #     print("Comp Index: ", ci['index'])
    #     print(ci)

    logging.info("Done constructing system components' info.")
    return sys_comp_info, comp_agent_mapping, flatten_colname_list, flatten_colname_list_agents

# TODO:10.21调试
# 样本数据的组织形式转换
def map_flatten_dict(organized_sample_one):
    comp_states_value = organized_sample_one[0]
    comp_actions_value = organized_sample_one[1]

    # DOUBLE CHECK
    if not len(comp_states_value) == len(comp_actions_value):
        logging.error("Unequal state and action info dimension during flatten mapping. Fix it now!")

    value_list = [sv for svs in comp_states_value for sv in svs] + [av for avs in comp_actions_value for av in avs]
    if len(organized_sample_one) > 2:  #带有reward项
        value_list.extend(organized_sample_one[2])
    return value_list

def sample_parse_flatten(organized_sample, flatten_colname_list, parse_batch_size=10):
    '''把仿真中，系统状态和系统行动flatten用于做存储，column_name的命名开头为 compindex_dimindex_feature_name，方便做反解析'''
    #organized_sample 是一个list，包含state+action+reward
    if parse_batch_size == 1: #如果单个样本（是个list），直接简单处理
        flattened_sample = map_flatten_dict(organized_sample)
    else:
        flattened_sample = map(map_flatten_dict, organized_sample)
    flattened_sample_df = pd.DataFrame(flattened_sample)
    flattened_sample_df.columns = flatten_colname_list

    #DEBUG
    print("Raw value:")
    print(organized_sample)
    print(flattened_sample_df)

    return flattened_sample_df

def split_agent_flatten_sample(flattened_sample_df, flatten_colname_list, agents, comp_agent_mapping):
    '''将训练样本按照agent区分的形式，用columns=[]进行切片'''
    agent_colname_list = [[]]*len(agents)
    with_reward = False
    if 'reward' in flattened_sample_df.columns.values.tolist():
        with_reward = True
    for colname in flatten_colname_list:
        comp_index = colname.split('_')[0]
        agent_index = comp_agent_mapping[comp_index]
        agent_colname_list[agent_index].append(colname)
        # 添加reward这一列
        if with_reward:
            agent_colname_list.append('reward')
    agent_flatten_df_list = []
    for agent_colnames in agent_colname_list:
        agent_flatten_df_list.append(flattened_sample_df.loc[:, agent_colnames])
    return agent_flatten_df_list

def revert_agent_comp_mapping(agents): #debug DONE
    comp_agent_mapping = {}
    a_cnt = 0
    for a in agents:
        for j in a:
            comp_agent_mapping[j] = a_cnt
        a_cnt += 1
    return comp_agent_mapping

# 对component config info添加是否需要embedding信息
def use_embedding_condition(comp_info):
    if conf.use_embed_condition(comp_info):
        return True
    return False

def add_use_embed_info(system_component_info):
    for i in range(len(system_component_info)):
        if use_embedding_condition(system_component_info[i]):
            system_component_info[i]['use_embedding'] = True
    return system_component_info

def select_best_action_agent(agent_pred_result, params, strategy = 'e-greedy'):
    '''对每个agent的一批action做选择，返回index'''
    if strategy == 'e-greedy':
        random_e = params['e']
        rand = random.random()
        if rand > random_e: #选cost最小的
            agent_best_action_index = agent_pred_result.index(min(agent_pred_result))
        else: #随机选一个
            agent_best_action_index = random.randrange(0, len(agent_pred_result))
    return agent_best_action_index

def print_dict_formatted(dict_data):
    '''将dict格式化输出，方便预览'''
    print(json.dumps(dict_data, indent=4))

# 暂时弃用的action设计方法
# comp_action_fc = [
#         # 第一维：维修活动对系统状态的提升量
#         {"component_index": comp_index,
#          "feature_name": comp_name + '_deterioration_action',
#          "dtype": 'int',
#          "method": categorical_int_method,
#          "use_embedding": True,
#          "embed_vec_size": ACTION_DETER_EMBED_VECSIZE,
#          "int_bucket_size": STATE_DETER_BUCKET_SIZE,
#          "network_usage": ['sparse']
#          },
#         # 第二维：是否进行更换
#         {"component_index": comp_index,
#          "feature_name": comp_name + '_isreplece_action',
#          "dtype": 'int',
#          "method": categorical_binary_method,
#          "use_embedding": True,
#          "embed_vec_size": ACTION_REPLACE_EMBED_VECSIZE,
#          "network_usage": ['sparse']
#          },
#
#         # 第三维：进行更换时，对部件故障率的提升程度
#         {"component_index": comp_index,
#          "feature_name": comp_name + '_failure_action',
#          "dtype": 'double',
#          "method": direct_numeric_method,
#          "use_embedding": False,
#          "network_usage": ['dense']
#          }
#     ]
