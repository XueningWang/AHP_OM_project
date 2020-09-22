#coding: utf-8
'''提供系统仿真相关的子函数'''

import logging
import numpy as np
import math

#指数函数随机数，逆函数法
def exp_rand(lam=1):
    u = np.random.uniform(0,1)
    return -np.log(u)/lam

#韦伯函数随机数，逆函数法
def weibull_rand(alpha=1,beta=1):
    u = np.random.uniform(0,1)
    return beta*math.pow(-np.log(u),1/alpha)

# 随机数生成器
# TODO:9.20 需要修改参数，将故障率提升之后对寿命分布的影响考虑在内
def generate_random_lifetime(distribution, dist_args, type='single', num=1):
    '''给出一个部件在某个状态上的寿命(WEIBULL)或疏水单位量两次产生的间隔时间(EXPONENTIAL)'''

    '''参数类型：distribution是字符串，="weibull"OR"exp"
                dist_args是字典类型（e.g. expp={'lambda':1}
                weibullp={"alpha":1,"beta":2}），key:value = 随机分布的参数名:参数值
                type = "single"OR"batch", batch指的是一次生成相同参数的一批随机数
                num默认=1，在type = "batch"的时候，代表一次生成几个数'''
    '''输出参数类型：type = "single"时是一个值，type = "batch"时是一个list'''
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

if __name__ == "__main__":
    expp = {'lambda': 1}
    weibullp = {"alpha": 1, "beta": 2}
    v = generate_random_lifetime('exp', expp, 'batch', 2)
    u = generate_random_lifetime('weibull', weibullp, 'batch', 3)
    print(v)
    print(u)
