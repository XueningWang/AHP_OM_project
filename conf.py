#coding: utf-8

'''该脚本独立配置系统参数和算法实现的超参数
author: Wang Xue-Ning'''

from utils import *

# 系统参数
## 系统结构
NUM_HEATING_PATH = 2
NUM_BY_PATH = 2
HEATER_PER_HP = 2
NUM_STATE_VALVE = 5
NUM_STATE_NONVALVE = 5
SYSTEM_COMPONENT = [
    {"index": 0, "name": 'HP_1_P', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "component_type": 'P', "num_states": NUM_STATE_VALVE},
    {"index": 1, "name": 'HP_1_Q', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "component_type": 'Q', "num_states": NUM_STATE_VALVE},
    {"index": 2, "name": 'HP_1_H1_H', "valve_type": 'NVL', "path_type": 'HP', "path_index": 1, "heater_index": 1, "component_type": 'H', "num_states": NUM_STATE_NONVALVE},
    {"index": 3, "name": 'HP_1_H1_K', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "heater_index": 1, "component_type": 'K', "num_states": NUM_STATE_VALVE},
    {"index": 4, "name": 'HP_1_H1_I', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "heater_index": 1, "component_type": 'I', "num_states": NUM_STATE_VALVE},
    {"index": 5, "name": 'HP_1_H1_J', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "heater_index": 1, "component_type": 'J', "num_states": NUM_STATE_VALVE},
    {"index": 6, "name": 'NHP_1_R', "valve_type": 'VL', "path_type": 'NHP', "path_index": 1, "component_type": 'R', "num_states": NUM_STATE_VALVE},
    #...以此类推，没有写完
]
COMPONENT_TYPE_MAPPING = {
    'P': '进口隔离阀',
    'Q': '出口隔离阀',
    'H': '加热器',
    'K': '疏水阀',
    'I': '抽汽阀',
    'J': '排汽阀',
    'R': '旁路阀'
}
AGENT_COMPONENTS = [[0,1,3,4,5], [], []] #只存index，一个AGENT作为一个子列表

## 寿命分布相关参数
LAMBDA = #一个值（如果所有部件参数统一）或一个列表（与SYSTEM_COMPONENT等长）或一个短列表（配置不同部件相同状态上用一组参数）
GAMMA =

'''其他需要的参数在这里加～'''
## 成本相关参数

## 打包
# SYSTEM_PARAMS = {'num_heating_path': NUM_HEATING_PATH,
#                  'num_by_path': NUM_BY_PATH,
#                  'heater_per_hp': HEATER_PER_HP,
#                  'num_state_valve': NUM_STATE_VALVE,
#                  'num_state_nonvalve': NUM_STATE_NONVALVE,
#                  'system_component': SYSTEM_COMPONENT,
#                  'component_type_mapping': COMPONENT_TYPE_MAPPING,
#                  'agent_components': AGENT_COMPONENTS,
#                  #...
#                  }

# 神经网络结构
## 结构版本筛选
NN_STRUCTURE_VERSION = 'wide_and_deep_v1' #如果有其他结构直接把名字添加在这里，并且在network_init里进行修改

## 超参数配置(wide and deep model) TODO:根据类的完整实现补充其他默认超参调整接口
WD_LINEAR_OPTIMIZER = 'Ftrl'
WD_DENSE_LAYERS = [512, 256, 128, 64]
WD_LEARNING_RATE = 0.01
WD_L1_REGULAR_STRENGTH = 0.001
WD_L2_REGULAR_STRENGTH = 0.001

# DRL训练
## 训练超参
BATCH_SIZE = #10
TERMINATION_NUM_ITERATION = 1000

## Termination条件
def is_terminate(num_iteration, type = 'num_iteration'):
    # 以迭代次数为标准结束循环
    if type == 'num_iteration':
        if num_iteration > TERMINATION_NUM_ITERATION:
            return True
    # TODO:其他标准
    # if some_condition
    return False

## 是否对每次的reward做值变换
def reward_trans(reward):
    return reward

## 离散编码的INT类型特征，分箱大小
STATE_DETER_BUCKET_SIZE = 2* max(NUM_STATE_VALVE, NUM_STATE_NONVALVE)

## 各embedding向量长度
STATE_DETER_EMBED_VECSIZE = STATE_DETER_BUCKET_SIZE
ACTION_DETER_EMBED_VECSIZE = STATE_DETER_BUCKET_SIZE
ACTION_REPLACE_EMBED_VECSIZE = 4

## 添加是否需要embedding信息
def use_embedding_condition(comp_info):
    if comp_info['component_type'] in ['H', 'K', 'R']:
        return True
    return False

for i in range(len(SYSTEM_COMPONENT)):
    if use_embedding_condition(SYSTEM_COMPONENT[i]):
        SYSTEM_COMPONENT[i]['use_embedding'] = True

## 从系统信息组织成特征信息
STATE_FEATURE_COLUMNS = []
ACTION_FEATURE_COLUMNS = []
for ac in AGENT_COMPONENTS:
    agent_state_fc = []
    agent_action_fc = []
    for comp_index in ac:
        comp_info = SYSTEM_COMPONENT[comp_index]
        comp_name = comp_info['name']
        comp_state_fc = [
            # 第一维，部件离散状态
            {"component_index": comp_index,
             "feature_name": comp_name+'_deterioration_state',
             "dtype": 'int',
             "method": categorical_int_method,
             "use_embedding": comp_info.get("state_use_embedding", False),
             "embed_vec_size": STATE_DETER_EMBED_VECSIZE,
             "int_bucket_size": STATE_DETER_BUCKET_SIZE,
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
                                  "feature_name": comp_name+'_isactive_state',
                                  "dtype": 'int',
                                  'method': categorical_binary_method,
                                  "use_embedding": False,
                                  "network_usage": ['dense']
                                  })

        comp_action_fc = [
            # 第一维：维修活动对系统状态的提升量
            {"component_index": comp_index,
             "feature_name": comp_name+'_deterioration_action',
             "dtype": 'int',
             "method": categorical_int_method,
             "use_embedding": True,
             "embed_vec_size": ACTION_DETER_EMBED_VECSIZE,
             "int_bucket_size": STATE_DETER_BUCKET_SIZE,
             "network_usage": ['sparse']
             },
            # 第二维：是否进行更换
            {"component_index": comp_index,
             "feature_name": comp_name+'_isreplecement_action',
             "dtype": 'int',
             "method": categorical_binary_method,
             "use_embedding": True,
             "embed_vec_size": ACTION_REPLACE_EMBED_VECSIZE,
             "network_usage": ['sparse']
             },

            # 第三维：进行更换时，对部件故障率的提升程度
            {"component_index": comp_index,
             "feature_name": comp_name+'_failure_action',
             "dtype": 'double',
             "method": direct_numeric_method,
             "use_embedding": False,
             "network_usage": ['dense']
             }
        ]
        agent_state_fc.append(comp_state_fc)
        agent_action_fc.append(comp_action_fc)

    STATE_FEATURE_COLUMNS.append(agent_state_fc)
    ACTION_FEATURE_COLUMNS.append(agent_action_fc)
