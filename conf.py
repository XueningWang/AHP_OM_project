#coding: utf-8

'''该脚本独立配置系统参数和算法实现的超参数
author: Wang Xue-Ning'''

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
AGENT_COMPONENTS = [[0,2,2,3,4,5], [], []] #只存index，一个AGENT作为一个子列表

## 寿命分布相关参数
LAMBDA = #一个值（如果所有部件参数统一）或一个列表（与SYSTEM_COMPONENT等长）或一个短列表（配置不同部件相同状态上用一组参数）
GAMMA =

'''其他需要的参数在这里加～'''
## 成本相关参数

## 打包
SYSTEM_PARAMS = {'num_heating_path': NUM_HEATING_PATH,
                 'num_by_path': NUM_BY_PATH,
                 'heater_per_hp': HEATER_PER_HP,
                 'num_state_valve': NUM_STATE_VALVE,
                 'num_state_nonvalve': NUM_STATE_NONVALVE,
                 'system_component': SYSTEM_COMPONENT,
                 'component_type_mapping': COMPONENT_TYPE_MAPPING,
                 'agent_components': AGENT_COMPONENTS}


# DRL训练
## 可调控属性
BATCH_SIZE = 10

## 打包
DRL_PARAMS = {}


# 神经网络相关参数
## 打包
NETWORK_PARAMS = {'batch_size': BATCH_SIZE,
                  }
