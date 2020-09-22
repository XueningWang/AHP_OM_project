#coding: utf-8
'''独立配置系统参数和算法实现的超参数'''

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
    {"index": 6, "name": 'HP_1_H2_H', "valve_type": 'NVL', "path_type": 'HP', "path_index": 1, "heater_index": 2, "component_type": 'H', "num_states": NUM_STATE_NONVALVE},
    {"index": 7, "name": 'HP_1_H2_K', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "heater_index": 2, "component_type": 'K', "num_states": NUM_STATE_VALVE},
    {"index": 8, "name": 'HP_1_H2_I', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "heater_index": 2, "component_type": 'I', "num_states": NUM_STATE_VALVE},
    {"index": 9, "name": 'HP_1_H2_J', "valve_type": 'VL', "path_type": 'HP', "path_index": 1, "heater_index": 2, "component_type": 'J', "num_states": NUM_STATE_VALVE},

    {"index": 10, "name": 'HP_2_P', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "component_type": 'P', "num_states": NUM_STATE_VALVE},
    {"index": 11, "name": 'HP_2_Q', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "component_type": 'Q', "num_states": NUM_STATE_VALVE},
    {"index": 12, "name": 'HP_2_H1_H', "valve_type": 'NVL', "path_type": 'HP', "path_index": 2, "heater_index": 1, "component_type": 'H', "num_states": NUM_STATE_NONVALVE},
    {"index": 13, "name": 'HP_2_H1_K', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "heater_index": 1, "component_type": 'K', "num_states": NUM_STATE_VALVE},
    {"index": 14, "name": 'HP_2_H1_I', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "heater_index": 1, "component_type": 'I', "num_states": NUM_STATE_VALVE},
    {"index": 15, "name": 'HP_2_H1_J', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "heater_index": 1, "component_type": 'J', "num_states": NUM_STATE_VALVE},
    {"index": 16, "name": 'HP_2_H2_H', "valve_type": 'NVL', "path_type": 'HP', "path_index": 2, "heater_index": 2, "component_type": 'H', "num_states": NUM_STATE_NONVALVE},
    {"index": 17, "name": 'HP_2_H2_K', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "heater_index": 2, "component_type": 'K', "num_states": NUM_STATE_VALVE},
    {"index": 18, "name": 'HP_2_H2_I', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "heater_index": 2, "component_type": 'I', "num_states": NUM_STATE_VALVE},
    {"index": 19, "name": 'HP_2_H2_J', "valve_type": 'VL', "path_type": 'HP', "path_index": 2, "heater_index": 2, "component_type": 'J', "num_states": NUM_STATE_VALVE},

    {"index": 20, "name": 'NHP_3_R', "valve_type": 'VL', "path_type": 'NHP', "path_index": 3, "component_type": 'R', "num_states": NUM_STATE_VALVE},
    {"index": 21, "name": 'NHP_3_R', "valve_type": 'VL', "path_type": 'NHP', "path_index": 3, "component_type": 'R', "num_states": NUM_STATE_VALVE},
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

## TODO:设计各种类部件性能函数，即g(S)。按照部件的种类划分（P,Q,H,K,I,J,R）
COMP_PERFORM_FUNC_P = lambda x: x
COMP_PERFORM_FUNC_Q = lambda x: x
COMP_PERFORM_FUNC_H = lambda x: x
COMP_PERFORM_FUNC_K = lambda x: x
COMP_PERFORM_FUNC_I = lambda x: x
COMP_PERFORM_FUNC_J = lambda x: x
COMP_PERFORM_FUNC_R = lambda x: x

## agent分布
AGENT_COMPONENTS = [[2,3,4,5], [6,7,8,9], [12,13,14,15], [16,17,18,19], [0,1,10,11,20,21]]

## TODO:寿命分布相关参数矫正
WEIBULL_BETA = {'P': 0.1, 'Q': 0.1, 'H': 0.2,'K': 0.3, 'I': 0.3, 'J': 0.3, 'R': 0.1}
WEIBULL_THETA = {'P': 0.01, 'Q': 0.01, 'H': 0.01,'K': 0.01, 'I': 0.01, 'J': 0.01, 'R': 0.01}
FAILURE_RATE_PARMS_a = 0.05
FAILURE_RATE_PARMS_b = 1.05
INFINITE_TIME = 99999
DRAINWATER_LAMBDA = 0.05

## TODO:疏水产生过程参数矫正
DRAINWATER_UNIT = 1


## TODO:成本相关参数
def cost_func(x):
    return x

# 神经网络结构
## 结构版本筛选
NN_STRUCTURE_VERSION = 'wide_and_deep_v1' #如果有其他结构直接把名字添加在这里，并且在network_init里进行修改

## 超参数配置(wide and deep model)
WD_LINEAR_OPTIMIZER = 'Ftrl'
WD_DENSE_LAYERS = [512, 256, 128, 64]
WD_LEARNING_RATE = 0.01
WD_L1_REGULAR_STRENGTH = 0.001
WD_L2_REGULAR_STRENGTH = 0.001

# DRL训练
## 训练超参
BATCH_SIZE = 10
TRAIN_EPOCHS = 1
IS_SHUFFLE = True
SHUFFLE_BUFFER_SIZE = 10000
TRAIN_VERBOSE_STEP = 10
MODEL_DIRS = ['models/model_agent_' + str(i+1) for i in range(len(AGENT_COMPONENTS))]

## Termination条件
MAX_TERMINATION_NUM_ITERATION = 100
TERMINATION_CRITERION = 'num_iteration'
def is_terminate(num_iteration, criterion = 'num_iteration', max_termination_num_iteration = 100000):
    # 以迭代次数为标准结束循环
    if criterion == 'num_iteration':
        if num_iteration > max_termination_num_iteration:
            return True
    # TODO:其他标准
    # if some_condition
    return False

## reward值变换方式
reward_trans_func = lambda reward: reward

## 离散编码的INT类型特征，分箱大小
STATE_DETER_BUCKET_SIZE = 2*max(NUM_STATE_VALVE, NUM_STATE_NONVALVE)

## 各embedding向量长度
STATE_DETER_EMBED_VECSIZE = STATE_DETER_BUCKET_SIZE
ACTION_DETER_EMBED_VECSIZE = STATE_DETER_BUCKET_SIZE
ACTION_REPLACE_EMBED_VECSIZE = 4

use_embed_condition = lambda info: info['component_type'] in ['H', 'K', 'R']

## 根据value选择行动策略
ACTION_SELECT_STRATEGY = 'e-greedy'
ACTION_SELECT_PARAMS = {'e': 0.1}

## 历史样本存储和回放
REPLAY_ONE_BATCH_SIZE = 10 #for test
REPLAY_BATCH_NUM = 3 #for test
REPLAY_AFTER_EPOCH = 50 #for test
