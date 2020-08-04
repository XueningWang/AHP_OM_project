#coding: utf-8
'''提供全局调度相关的子函数'''

import pandas as pd
import logging

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
    if comp_info['component_type'] == "R":  # 疏水器单独加第三维特征，表示是否为备件状态
        comp_state_fc.append({"component_index": comp_index,
                              "feature_name": comp_name + '_isactive_state',
                              "dtype": 'int',
                              'method': categorical_binary_method,
                              "use_embedding": False,
                              "network_usage": ['dense']
                              })
    comp_action_fc = [
        # 第一维：维修活动对系统状态的提升量
        {"component_index": comp_index,
         "feature_name": comp_name + '_deterioration_action',
         "dtype": 'int',
         "method": categorical_int_method,
         "use_embedding": True,
         "embed_vec_size": ACTION_DETER_EMBED_VECSIZE,
         "int_bucket_size": STATE_DETER_BUCKET_SIZE,
         "network_usage": ['sparse']
         },
        # 第二维：是否进行更换
        {"component_index": comp_index,
         "feature_name": comp_name + '_isreplecement_action',
         "dtype": 'int',
         "method": categorical_binary_method,
         "use_embedding": True,
         "embed_vec_size": ACTION_REPLACE_EMBED_VECSIZE,
         "network_usage": ['sparse']
         },

        # 第三维：进行更换时，对部件故障率的提升程度
        {"component_index": comp_index,
         "feature_name": comp_name + '_failure_action',
         "dtype": 'double',
         "method": direct_numeric_method,
         "use_embedding": False,
         "network_usage": ['dense']
         }
    ]
    return comp_state_fc, comp_action_fc

# 样本数据的组织形式转换
def map_flatten_dict(organized_sample_one):
    comp_states_value = organized_sample_one[0]
    comp_actions_value = organized_sample_one[1]

    # DOUBLE CHECK
    if not len(comp_states_value) == len(comp_actions_value):
        logging.error("Unequal state and action info dimension during flatten mapping. Fix it now!")

    flattened_dict = {}
    for comp_index in range(len(comp_states_value)):
        comp_info = conf.SYSTEM_COMPONENT[comp_index]
        state_info, action_info = feature_column_struct(comp_info)
        column_prefix = str(comp_index)+'_'
        for state_index in range(len(comp_states_value)):
            flattened_dict[column_prefix + str(state_index) + '_' + state_info[state_index]['feature_name']] = comp_states_value[comp_index][state_index]
        for action_index in range(len(comp_actions_value)):
            flattened_dict[column_prefix + str(action_index) + '_' + state_info[action_index]['feature_name']] = comp_actions_value[comp_index][action_index]
    if len(organized_sample_one) > 2:  #带有reward项
        flattened_dict['reward'] = organized_sample_one[2]
    return flattened_dict

def sample_parse_flatten(organized_sample, parse_batch_size=1):
    '''把仿真中，系统状态和系统行动flatten用于做存储，column_name的命名开头为 compindex_dimindex_feature_name，方便做反解析'''
    #organized_sample 是一个list，包含state+action+reward
    if parse_batch_size == 1: #如果单个样本（是个list），直接简单处理
        flattened_sample = map_flatten_dict(organized_sample)
    else:
        flattened_sample = map(map_flatten_dict, organized_sample)
    flattened_sample_df = pd.DataFrame.from_dict(flattened_sample)
    return flattened_sample_df

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
