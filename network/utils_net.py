#coding:utf-8
'''提供深度神经网络相关的子函数'''

import tensorflow as tf
import pandas as pd
import logging
import sys

sys.path.append('../')
import conf

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
