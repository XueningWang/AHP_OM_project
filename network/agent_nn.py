#coding: utf-8

import tensorflow as tf
import logging
import sys

sys.path.append('../')
from utils import *
import conf

class AgentDeepNetwork:
    def __init__(self, agent_index):
        self.conf = conf
        self.agent_index = agent_index
        self.agent_comp_index = conf.AGENT_COMPONENTS[agent_index]
        self.agent_state_info = conf.STATE_FEATURE_COLUMNS[agent_index]
        self.agent_action_info = conf.ACTION_FEATURE_COLUMNS[agent_index]
        self.estimator = 0  #神经网络占位

    def network_init(self):
        '''按照配置，构建一个神经网络结构'''
        # CHECK
        if not len(self.agent_state_info) == len(self.agent_action_info):
            logging.error("Unequal state and action info dimension during init step. Fix it now!")

        # 构建网络结构
        if self.conf.NN_STRUCTURE_VERSION == 'wide_and_deep_v1':
            sparse_fc = []
            dense_fc = []
            for info in [self.agent_state_info, self.agent_action_info]:
                feature_name = info['feature_name']
                method = info['method']
                bucket_size = info.get('int_bucket_size', 0)
                network_usage = info['network_usage']
                isembed = info.get('use_embedding', False)
                feature_column = method(feature_name, bucket_size)
                if isembed:
                    embed_vec_size = info.get('embed_vec_size', 8)
                    feature_column = tf.feature_column.embedding_column(feature_column, dimension = embed_vec_size)
                if 'sparse' in network_usage:
                    sparse_fc.append(feature_column)
                if 'dense' in network_usage:
                    dense_fc.append(feature_column)

            # 配置神经网络结构
            estimator = tf.estimator.DNNLinearCombinedRegressor(
                # sparse settings
                linear_feature_columns=sparse_fc,
                linear_optimizer=conf.WD_LINEAR_OPTIMIZER,
                # dense settings
                dnn_feature_columns=dense_fc,
                dnn_hidden_units=conf.WD_DENSE_LAYERS,
                dnn_optimizer=tf.train.ProximalAdagradOptimizer(
                    learning_rate = conf.WD_LEARNING_RATE,
                    l1_regularization_strength=conf.WD_L1_REGULAR_STRENGTH,
                    l2_regularization_strength=conf.WD_L2_REGULAR_STRENGTH),
            )
            self.estimator = estimator


    def process_one_sample(self, agent_state, agent_action, agent_cost):
        '''对输入的batch sample转换成送入神经网络训练的数据格式(feature & label)'''

        # 处理Feature
        feature = {}

        # CHECK
        if not len(agent_state) == len(agent_action):
            logging.error("Unequal state and action dimension. Fix it now!")

        for i in range(len(agent_state)): #第i个部件
            for j in range(len(agent_state[i])): #第j个状态维度
                element_info = self.agent_state_info[i][j]
                s_feature_name = element_info['feature_name']
                s_feature_dtype = element_info['dtype']
                s_feature_value = gen_feature_value(agent_state[i][j], s_feature_dtype)
                feature[s_feature_name] = s_feature_value
            for k in range(len(agent_state[i])):
                element_info = self.agent_action_info[i][k]
                a_feature_name = element_info['feature_name']
                a_feature_dtype = element_info['dtype']
                a_feature_value = gen_feature_value(agent_action[i][k], a_feature_dtype)
                feature[a_feature_name] = a_feature_value

        # 处理Label
        label = tf.cast(reward_trans(agent_cost), tf.float32)

        return feature, label

    def batch_train(self):
        '''训练模型的核心逻辑'''

    def save_model(self):
        '''模型固化或以现有参数持久化，如果不做任何操作就能保存现有参数，这个就不用了'''

    def save_batch_sample(self):
        '''保存输入的batch sample，后续可用于memory replay'''

    def memory_replay(self):
        '''从储存的过去SAMPLE中拿一部分，merge到batch_train中训练'''

    def _batch_train(self):
        '''给定一个batch的样本，对神经网络训练并保存模型参数，以备后面预测用'''

    def _predict(self):
        '''给定一个输入，返回输出'''
