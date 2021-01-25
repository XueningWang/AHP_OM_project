import sympy as sym
import copy

from utils_sys_v3 import *
from utils_global_v2 import *

# 测试参数
wb_para_beta, wb_para_theta = 2.5, 0.5
para_a, para_b = 0.1, 1.2
para_c = 2.0
load_lower_wl, load_upper_wu = 0, 1
## 系统串并联结构
simple_sys_comp_index = [0, 2, 3, 10, 11, 13, 26, 27, 28]
simple_sys_structure = {    # s for 串联，p for 并联, b for base（仅一部件）
                            'sub1':
                                {
                                    'sub11': {'comp': 0, 'type': 'b'},
                                    'sub12':
                                        {
                                            'sub121': {'comp': 2, 'type': 'b'},
                                            'sub122': {'comp': 3, 'type': 'b'},
                                            'type': 's', # s
                                        },
                                     'type': 'p'
                                },
                            'sub2':
                                {
                                    'sub21':
                                        {
                                            'sub211': {'comp': 10, 'type': 'b'},
                                            'sub212': {'comp': 11, 'type': 'b'},
                                            'type': 'p',
                                        },
                                    'sub22': {'comp': 13, 'type': 'b'},
                                    'type': 's' # s
                                },
                            'type': 's'} #s

# 作图参数
hazard_rate_y_ulim = 10000



# test 威布尔分布
t_points = range(0, 100, 1)
time_t = sym.symbols('t')
fn_h = form_weibull_rate_fn(wb_para_beta, wb_para_theta)
wb_y_points = [fn_h.evalf(subs = {time_t: t_value}) for t_value in t_points]

plot_scatter_chart(t_points, wb_y_points, "Weibull hazard rate, beta %.2f theta %.2f" %(wb_para_beta, wb_para_theta),
                   y_ulim = hazard_rate_y_ulim)

# test Hybrid hazard rate随维修变化曲线、Load sharing 对hazard rate改变
## 参数设置
update_time_list = [30, 50, 60]
num_comp_n, num_fcomp_nf = 10, 4
load_total_W = 0.6

update_time_list_record = copy.deepcopy(update_time_list)
last_update_time = 0
next_update_time = update_time_list.pop(0)
hybrid_y_points = []
lshared_y_points = []
lshared_fn_h = calc_load_share_hazard_rate_fn(fn_h,
                                              para_c, num_comp_n, num_fcomp_nf,
                                              load_total_W, load_lower_wl, load_upper_wu)
for t_value in t_points:
    if t_value == next_update_time and t_value > 0: #初始状态不更新
        fn_h = calc_hybrid_hazard_rate_fn(fn_h, para_a, para_b, t_value - last_update_time)
        lshared_fn_h = calc_load_share_hazard_rate_fn(fn_h,
                                                      para_c, num_comp_n, num_fcomp_nf,
                                                      load_total_W, load_lower_wl, load_upper_wu)
        last_update_time = t_value
        next_update_time = update_time_list.pop(0) if len(update_time_list) > 0 else len(t_points)
    virtual_age = t_value - last_update_time
    hybrid_y_points.append(fn_h.evalf(subs = {time_t: virtual_age}))
    lshared_y_points.append(lshared_fn_h.evalf(subs = {time_t: virtual_age}))

str_t_points = ','.join([str(i) for i in update_time_list_record])
plot_scatter_chart(t_points, hybrid_y_points, "Hybrid hazard rate, update points %s"%str_t_points,
                   y_ulim = hazard_rate_y_ulim)
plot_scatter_chart(t_points, lshared_y_points, "Hybrid hazard rate (load shared), update points %s"%str_t_points,
                   y_ulim = hazard_rate_y_ulim)

# test UGF 计算
## 模拟部件可靠性值
relia_value_comps = {0: 0.280, 2: 0.083, 3: 0.928, 10: 0.003, 11: 0.234, 13: 0.794, 26: 0.542, 27: 0.001, 28: 0.836}
simple_sys_UGF = calc_sys_UGF_binary(simple_sys_structure, relia_value_comps)
print(simple_sys_UGF)
