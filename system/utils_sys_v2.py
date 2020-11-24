'''提供系统仿真相关的子函数（新）'''

def gen_comp_state(system_comp_info, bypath_comp, deter_state, failure_rate, bypath_spare):
    state = [[deter_state[i], failure_rate[i]] for i in range(system_comp_info)]
    bypath_vl_index = 0
    for bci in bypath_comp:
        state[bci].append(bypath_spare[bypath_vl_index])
        bypath_vl_index += 1
    return state

#指数函数随机数，逆函数法
def exp_rand(lam=1):
    u = np.random.uniform(0,1)
    return -np.log(u)/lam

#韦伯函数随机数，逆函数法
def weibull_rand(alpha=1,beta=1):
    u = np.random.uniform(0,1)
    return beta*math.pow(-np.log(u),1/alpha)

def generate_random_lifetime(distribution, dist_args, type='single', num=1):
    '''给出一个部件在某个状态上的寿命(WEIBULL)或疏水单位量两次产生的间隔时间(EXPONENTIAL)'''
    if distribution == "exp":
        lam = dist_args['lambda'] #NOTE:8.7精简了一下传参方式，测试通过

        if type == 'single':
            value = exp_rand(lam)
        else:
            value = np.zeros(num)
            for i in range(0, num):
                value[i] = exp_rand(lam)

    elif distribution == "weibull":
        alpha = dist_args['alpha']
        beta = dist_args['beta']

        if type == 'single':
            value = weibull_rand(alpha, beta)
        else:
            value = np.zeros(num)
            for i in range(0, num):
                value[i] = weibull_rand(alpha, beta)
    else:
        value = -1
    return value
