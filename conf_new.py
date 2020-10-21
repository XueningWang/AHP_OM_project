#coding: utf-8
'''独立配置系统参数和算法实现的超参数；适用20202.10更新的系统建模设置'''

NUM_HEATING_PATH = 2
NUM_BY_PATH = 2
HEATER_PER_HP = 2
NUM_STATE_VALVE = 2
NUM_STATE_NONVALVE = 5

SYSTEM_COMPONENT = [
    {"index": 0, "sub_sys": "H_sys", "comp_name": "H_NH1_S", "real_name": "008VL", "valve_type": "VL", "comp_type": "S"},
    {"index": 1, "sub_sys": "H_sys", "comp_name": "H_NH2_S", "real_name": "009VL", "valve_type": "VL", "comp_type": "S"},
    {"index": 2, "sub_sys": "H_sys", "comp_name": "H_HT1_P", "real_name": "101VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 3, "sub_sys": "H_sys", "comp_name": "H_HT1_R", "real_name": "601RE", "valve_type": "NVL", "comp_type": "R"},
    {"index": 4, "sub_sys": "H_sys", "comp_name": "H_HT2_P", "real_name": "102VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 5, "sub_sys": "H_sys", "comp_name": "H_HT2_R", "real_name": "701RE", "valve_type": "NVL", "comp_type": "R"},
    {"index": 6, "sub_sys": "H_sys", "comp_name": "H_HT3_P", "real_name": "201VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 7, "sub_sys": "H_sys", "comp_name": "H_HT3_R", "real_name": "602RE", "valve_type": "NVL", "comp_type": "R"},
    {"index": 8, "sub_sys": "H_sys", "comp_name": "H_HT4_P", "real_name": "202VL", "valve_type": "VL", "comp_type": "P"},
    {"index": 9, "sub_sys": "H_sys", "comp_name": "H_HT4_R", "real_name": "702RE", "valve_type": "NVL", "comp_type": "R"},

    {"index": 10, "sub_sys": "D_sys", "comp_name": "S_HT1_K", "real_name": "117VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 11, "sub_sys": "D_sys", "comp_name": "S_HT1_L", "real_name": "118VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 12, "sub_sys": "D_sys", "comp_name": "S_HT1_M", "real_name": "134VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 13, "sub_sys": "D_sys", "comp_name": "S_HT1_N", "real_name": "601BA", "valve_type": "NVL", "comp_type": "N"},
    {"index": 14, "sub_sys": "D_sys", "comp_name": "S_HT2_K", "real_name": "119VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 15, "sub_sys": "D_sys", "comp_name": "S_HT2_L", "real_name": "120VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 16, "sub_sys": "D_sys", "comp_name": "S_HT2_M", "real_name": "135VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 17, "sub_sys": "D_sys", "comp_name": "S_HT2_N", "real_name": "701BA", "valve_type": "NVL", "comp_type": "N"},
    {"index": 18, "sub_sys": "D_sys", "comp_name": "S_HT3_K", "real_name": "217VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 19, "sub_sys": "D_sys", "comp_name": "S_HT3_L", "real_name": "218VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 20, "sub_sys": "D_sys", "comp_name": "S_HT3_M", "real_name": "234VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 21, "sub_sys": "D_sys", "comp_name": "S_HT3_N", "real_name": "602BA", "valve_type": "NVL", "comp_type": "N"},
    {"index": 22, "sub_sys": "D_sys", "comp_name": "S_HT4_K", "real_name": "219VL", "valve_type": "VL", "comp_type": "K"},
    {"index": 23, "sub_sys": "D_sys", "comp_name": "S_HT4_L", "real_name": "220VL", "valve_type": "VL", "comp_type": "L"},
    {"index": 24, "sub_sys": "D_sys", "comp_name": "S_HT4_M", "real_name": "235VL", "valve_type": "VL", "comp_type": "M"},
    {"index": 25, "sub_sys": "D_sys", "comp_name": "S_HT4_N", "real_name": "702BA", "valve_type": "NVL", "comp_type": "N"},

    {"index": 26, "sub_sys": "S_sys", "comp_name": "D_PT1_U", "real_name": "001VV", "valve_type": "VL", "comp_type": "U"},
    {"index": 27, "sub_sys": "S_sys", "comp_name": "D_HT1_V", "real_name": "101VV", "valve_type": "VL", "comp_type": "V"},
    {"index": 28, "sub_sys": "S_sys", "comp_name": "D_HT3_V", "real_name": "201VV", "valve_type": "VL", "comp_type": "V"},
    {"index": 29, "sub_sys": "S_sys", "comp_name": "D_PT2_U", "real_name": "002VV", "valve_type": "VL", "comp_type": "U"},
    {"index": 30, "sub_sys": "S_sys", "comp_name": "D_HT2_V", "real_name": "103VV", "valve_type": "VL", "comp_type": "V"},
    {"index": 31, "sub_sys": "S_sys", "comp_name": "D_HT4_V", "real_name": "203VV", "valve_type": "VL", "comp_type": "V"},
]

COMPONENT_TYPE_MAPPING = {
    'P': '进口隔离阀',
    'Q': '出口隔离阀',
    'R': '加热器',
    'S': '旁路阀',

    'K': '疏水阀',
    'L': '应急疏水阀',
    'M': '疏水隔离阀',
    'N': '高压加热疏水箱',

    'U': '抽汽逆止阀',
    'V': '抽汽隔离阀',
}

AGENT_COMPONENTS = []

