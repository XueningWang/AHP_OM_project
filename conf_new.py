#coding: utf-8
'''独立配置系统参数和算法实现的超参数；适用20202.10更新的系统建模设置'''

NUM_HEATING_PATH = 2
NUM_BY_PATH = 2
HEATER_PER_HP = 2
NUM_STATE_VALVE = 2
NUM_STATE_NONVALVE = 5

SYSTEM_COMPONENT = [
    {"index": 0, "sub_sys": "H_sys", "name": "H_NH1_S", "real_name": "008VL", "valve_type": "VL", "comp_type": "S"},
    {"index": 1, "sub_sys": "H_sys", "name": "H_NH2_S", "real_name": "009VL", "valcve_type": "VL", "comp_type": "S"},
    {"index": 2, "sub_sys": "H_sys", "name": "H_HT1_P", "real_name": "101VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 3, "sub_sys": "H_sys", "name": "H_HT1_RH", "real_name": "601RE_H", "valve_type": "NVL", "comp_type": "RH"},
    {"index": 4, "sub_sys": "H_sys", "name": "H_HT1_RD", "real_name": "601RE_D", "valve_type": "NVL", "comp_type": "RD"},
    {"index": 5, "sub_sys": "H_sys", "name": "H_HT1_RS", "real_name": "601RE_S", "valve_type": "NVL", "comp_type": "RS"},
    {"index": 6, "sub_sys": "H_sys", "name": "H_HT2_P", "real_name": "102VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 7, "sub_sys": "H_sys", "name": "H_HT2_RH", "real_name": "701RE_H", "valve_type": "NVL", "comp_type": "RH"},
    {"index": 8, "sub_sys": "H_sys", "name": "H_HT2_RD", "real_name": "701RE_D", "valve_type": "NVL", "comp_type": "RD"},
    {"index": 9, "sub_sys": "H_sys", "name": "H_HT2_RS", "real_name": "701RE_S", "valve_type": "NVL", "comp_type": "RS"},
    {"index": 10, "sub_sys": "H_sys", "name": "H_HT3_P", "real_name": "201VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 11, "sub_sys": "H_sys", "name": "H_HT3_RH", "real_name": "602RE_H", "valve_type": "NVL", "comp_type": "RH"},
    {"index": 12, "sub_sys": "H_sys", "name": "H_HT3_RD", "real_name": "602RE_D", "valve_type": "NVL", "comp_type": "RD"},
    {"index": 13, "sub_sys": "H_sys", "name": "H_HT3_RS", "real_name": "602RE_S", "valve_type": "NVL", "comp_type": "RS"},
    {"index": 14, "sub_sys": "H_sys", "name": "H_HT4_P", "real_name": "202VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 15, "sub_sys": "H_sys", "name": "H_HT4_RH", "real_name": "702RE_H", "valve_type": "NVL", "comp_type": "RH"},
    {"index": 16, "sub_sys": "H_sys", "name": "H_HT4_RD", "real_name": "702RE_D", "valve_type": "NVL", "comp_type": "RD"},
    {"index": 17, "sub_sys": "H_sys", "name": "H_HT4_RS", "real_name": "702RE_S", "valve_type": "NVL", "comp_type": "RS"},

    {"index": 18, "sub_sys": "D_sys", "name": "S_HT1_K", "real_name": "117VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 19, "sub_sys": "D_sys", "name": "S_HT1_L", "real_name": "118VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 20, "sub_sys": "D_sys", "name": "S_HT1_M", "real_name": "134VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 21, "sub_sys": "D_sys", "name": "S_HT1_N", "real_name": "601BA", "valve_type": "NVL", "comp_type": "N"},
    {"index": 22, "sub_sys": "D_sys", "name": "S_HT2_K", "real_name": "119VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 23, "sub_sys": "D_sys", "name": "S_HT2_L", "real_name": "120VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 24, "sub_sys": "D_sys", "name": "S_HT2_M", "real_name": "135VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 25, "sub_sys": "D_sys", "name": "S_HT2_N", "real_name": "701BA", "valve_type": "NVL", "comp_type": "N"},
    {"index": 26, "sub_sys": "D_sys", "name": "S_HT3_K", "real_name": "217VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 27, "sub_sys": "D_sys", "name": "S_HT3_L", "real_name": "218VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 28, "sub_sys": "D_sys", "name": "S_HT3_M", "real_name": "234VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 29, "sub_sys": "D_sys", "name": "S_HT3_N", "real_name": "602BA", "valve_type": "NVL", "comp_type": "N"},
    {"index": 30, "sub_sys": "D_sys", "name": "S_HT4_K", "real_name": "219VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 31, "sub_sys": "D_sys", "name": "S_HT4_L", "real_name": "220VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 32, "sub_sys": "D_sys", "name": "S_HT4_M", "real_name": "235VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 33, "sub_sys": "D_sys", "name": "S_HT4_N", "real_name": "702BA", "valve_type": "NVL", "comp_type": "N"},

    {"index": 34, "sub_sys": "S_sys", "comp_name": "D_PT1_U", "real_name": "001VV", "valve_type": "VL", "comp_type": "U"},
    {"index": 35, "sub_sys": "S_sys", "comp_name": "D_HT1_V", "real_name": "101VV", "valve_type": "VL", "comp_type": "V"},
    {"index": 36, "sub_sys": "S_sys", "comp_name": "D_HT3_V", "real_name": "201VV", "valve_type": "VL", "comp_type": "V"},
    {"index": 37, "sub_sys": "S_sys", "comp_name": "D_PT2_U", "real_name": "002VV", "valve_type": "VL", "comp_type": "U"},
    {"index": 38, "sub_sys": "S_sys", "comp_name": "D_HT2_V", "real_name": "103VV", "valve_type": "VL", "comp_type": "V"},
    {"index": 39, "sub_sys": "S_sys", "comp_name": "D_HT4_V", "real_name": "203VV", "valve_type": "VL", "comp_type": "V"},
]

COMPONENT_TYPE_MAPPING = {
    'P': '进口隔离阀',
    'Q': '出口隔离阀',
    'RH': '加热器加热系统部分',
    'RD': '加热器疏水系统部分',
    'RS': '加热器抽汽系统部分',
    'S': '旁路阀',

    'K': '疏水阀',
    'L': '应急疏水阀',
    'M': '疏水隔离阀',
    'N': '高压加热疏水箱',

    'U': '抽汽逆止阀',
    'V': '抽汽隔离阀',
}
BYPATH_COMP = [0,1]
AGENT_COMPONENTS = [[0,1], [2,3,4,5], [6,7,8,9], [10,11,12,13], [14,15,16,17],
                    [18,19,20,21,22,23,24,25], [26,27,28,29,30,31,32,33],
                    [34,35,36], [37,38,39]] #划分方法见算法设计文档

## TODO:寿命分布相关参数矫正（按照部件类型区分）
INITIAL_LAMBDA = {'P': 0.1, 'Q': 0.1, 'RH': 0.2,'RD': 0.3, 'RS': 0.3, 'S': 0.3,
                  'K': 0.1, 'L':0.1, 'M': 0.1, 'N':0.1,
                  'U': 0.1, 'V':0.1}
# FAILURE_RATE_PARMS_a = {'P': 0.05, 'Q': 0.05, 'RH': 0.05,'RD': 0.05, 'RS': 0.05, 'S': 0.05,
#                         'K': 0.05, 'L': 0.05, 'M': 0.05, 'N': 0.05,
#                         'U': 0.05, 'V': 0.05}
# FAILURE_RATE_PARMS_b = {'P': 1.05, 'Q': 1.05, 'RH': 1.05,'RD': 1.05, 'RS': 1.05, 'S': 1.05,
#                         'K': 1.05, 'L': 1.05, 'M': 1.05, 'N': 1.05,
#                         'U': 1.05, 'V': 1.05}

FAILURE_RATE_FACTOR = 1.1
failure_augment_fn = lambda x : x*FAILURE_RATE_FACTOR
INFINITE_TIME = 99999

## TODO:成本相关参数设置
def cost_func(action_record):
    # 进行了视情维修
    CBM_cost = 0
    # 进行了机会维修
    OM_cost = 0
    # 直接更换
    RE_cost = 0
    return CBM_cost + OM_cost + RE_cost

# 神经网络相关

