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

def calc_comp_reliability_value():
    return 0

if __name__ == "__main__":
    wb_para_beta, wb_para_theta = 1.5, 0.5
    fn_h = form_weibull_rate_fn(wb_para_beta, wb_para_theta)
    sym.pprint(fn_h)
    fn_h_updated = calc_hybrid_hazard_rate_fn(fn_h, 0.2, 1.6, 10)
    sym.pprint(fn_h_updated)
    fn_h_lshared = calc_load_share_hazard_rate_fn(fn_h_updated, 2, 10, 4, 6, 4, 9)
    sym.pprint(fn_h_lshared)
