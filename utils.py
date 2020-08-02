#coding: utf-8
import tensorflow as tf
import logging

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

# 特征数据处理方法定义
def direct_numeric_method(key, bucket_size_fake):
    return tf.feature_column.numeric_column(key)

def categorical_binary_method(key, bucket_size_fake):
    return tf.feature_column.categorical_column_with_identity(key, num_buckets = 2)

def categorical_int_method(key, bucket_size):
    return tf.feature_column.categorical_column_with_hash_bucket(key, hash_bucket_size = bucket_size, dtype = tf.int32)

# 特征数据抽取
def gen_feature_value(value, dtype = 'int'):
    if dtype == 'int':
        value = tf.cast(value, tf.int32)
    elif dtype == 'double':
        value = tf.cast(value, tf.float32)
    else:
        logging.error("Invalid feature dtype. Fix it now!")
        value = 0
    return value

# 样本数据的组织形式转换。TODO:高频需求，注意数据结构使用及效率优化
def sample_parse_flatten(flattened_sample, parse_batch_size=1):
    '''把仿真中，系统状态和系统行动flatten用于做存储，注意column_name的命名要方便做反解析'''
    if parse_batch_size == 1: #如果单个样本，直接简单处理
    return 0

def sample_parse_organize(organized_sample, parse_batch_size=1):
    '''把存储的扁平化数据变成系统仿真中的格式'''
    if parse_batch_size == 1:
    return 0

def sample_parse_agents(organized_sample, parse_batch_size=1):
    '''把系统仿真中的数据格式，按照agent进行切分，组织成多个agent的list一起返回'''
    if parse_batch_size == 1:
    samples_agent = []
    return samples_agent
