#coding: utf-8


# 随机数生成器（WEIBULL/EXPOTENTIAL两种），给定随机分布类型、随机分布参数，生成一个或批量生成（BATCH）n个随机数。

def generate_random_lifetime(distribution, dist_args, type = 'single', num = 1):
    '''给出一个部件在某个状态上的寿命(WEIBULL)或疏水单位量两次产生的间隔时间(EXPONENTIAL)'''

    '''参数类型：distribution是字符串，="weibull"OR"exp"
                dist_args是字典类型，key:value = 随机分布的参数名:参数值
                type = "single"OR"batch", batch指的是一次生成相同参数的一批随机数
                num默认=1，在type = "batch"的时候，代表一次生成几个数'''
    '''输出参数类型：type = "single"时是一个值，type = "batch"时是一个list'''
    
    '''注意：WEIBULL分布和EXP分布是故障率分布，需要根据weibull分布和exp分布到寿命分布的关系式，生成物理含义是"寿命"的值'''

    return value
