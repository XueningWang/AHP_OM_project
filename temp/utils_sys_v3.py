import sympy as sym
sym.init_printing(use_latex=True)

def form_weibull_rate_fn(para_beta, para_theta):
    # 参数范围检查
    if para_beta <= 0 or para_theta <= 0:
        print("Invalid parameter value!")
        return 0
    time_t = sym.symbols('t')
    fn_h = para_beta/para_theta * (time_t/para_theta)**(para_beta-1)
    return fn_h

def calc_hybrid_hazard_rate_fn(fn_h, para_a, para_b, age_added_T):
    time_t = sym.symbols('t')
    fn_h = fn_h.subs(time_t, time_t + para_a * age_added_T)
    new_fn_h = para_b * fn_h
    return new_fn_h

def calc_load_share_hazard_rate_fn(fn_h,
                                   para_c, num_comp_n, num_fcomp_nf,
                                   load_total_W, load_lower_wl, load_upper_wu):
    return fn_h * para_c**((num_comp_n - num_fcomp_nf)/num_comp_n * (load_total_W - load_lower_wl) / (load_upper_wu - load_lower_wl))

def calc_comp_reliability_value(fn_h, t_value): # 可靠性：基于当前hazard rate，在t_value前保持不failure的概率
    time_t = sym.symbols('t')
    rel_value = sym.exp(- sym.integrate(fn_h, (time_t, 0, t_value)))
    return rel_value

def calc_twofold_perf_value_binary(rela_type, Phi_a, Phi_b):
    if rela_type == 's':
        return min(Phi_a, Phi_b)
    elif rela_type == 'p':
        return Phi_a + Phi_b

def calc_sys_perf_value_binary(sub_sys_structure, state_value_comps):
    # 递归求解系统表现函数
    def traverse_comp_recursive(sub_structure_dict):
        type = sub_structure_dict.get('type')
        if type == 'b':
            local_Phi = state_value_comps[sub_structure_dict['comp']] #该部件当前状态（二态）
        elif type == 's':
            local_Phi = min([traverse_comp_recursive(v) for k,v in sub_structure_dict.items() if k.startswith('sub')])
        elif type == 'p':
            local_Phi = sum([traverse_comp_recursive(v) for k,v in sub_structure_dict.items() if k.startswith('sub')])
        return local_Phi
    return traverse_comp_recursive(sub_sys_structure)

def calc_twofold_UGF_binary(expr_u_1, expr_u_2, rela_type):
    # 思路：先解析出表达式中带有的所有参数（系数和次数），然后手动计算一个外积，再生成表达式并化简
    coef_p_list_1 = []
    coef_g_list_1 = []
    coef_p_list_2 = []
    coef_g_list_2 = []
    for i in range(len(coef_p_list_1)):
        for j in range(len(coef_p_list_2)):

    return res_expr

def calc_sys_UGF_binary():
    #对每个sub_sys的返回值应当是ugf的表达式；>2个元素时应当逐步计算
    return 0

if __name__ == "__main__":
    wb_para_beta, wb_para_theta = 2.5, 0.5
    fn_h = form_weibull_rate_fn(wb_para_beta, wb_para_theta)
    sym.pprint(fn_h)
    fn_h_updated = calc_hybrid_hazard_rate_fn(fn_h, 0.2, 1.6, 10)
    sym.pprint(fn_h_updated)
    fn_h_lshared = calc_load_share_hazard_rate_fn(fn_h_updated, 2, 10, 4, 6, 4, 9)
    sym.pprint(fn_h_lshared)
    rel_value = calc_comp_reliability_value(fn_h, 1)
    print(rel_value)
