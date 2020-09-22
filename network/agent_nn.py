#coding: utf-8
'''深度神经网络类实现'''

import tensorflow as tf
import logging
import sys

sys.path.append('../')
import conf
from .utils_net import *

class AgentDeepNetwork:
    def __init__(self, agent_index, agent_comp_index, agent_comp_info):
        self.agent_index = agent_index
        self.agent_comp_index = agent_comp_index
        self.agent_comp_info = agent_comp_info
        self.batch_size = conf.BATCH_SIZE
        self.train_epochs = conf.TRAIN_EPOCHS
        self.is_shuffle = conf.IS_SHUFFLE
        self.shuffle_buffer_size = conf.SHUFFLE_BUFFER_SIZE
        self.train_verbose_step = conf.TRAIN_VERBOSE_STEP
        self.model_dir = conf.MODEL_DIRS[agent_index]

    def init_network(self):
        '''按照配置，构建一个神经网络结构'''
        # 构建网络结构
        if self.conf.NN_STRUCTURE_VERSION == 'wide_and_deep_v1':
            sparse_fc = []
            dense_fc = []
            for comp_info in self.agent_comp_info:
                for info in [comp_info['comp_state_fc'], comp_info['comp_action_info']]:
                    feature_name = info['flatten_column_name']
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

            # 配置神经网络训练config
            config = tf.estimator.RunConfig(
                keep_checkpoint_max=3,
                model_dir=self.model_dir,
                save_checkpoints_secs=600,
                save_summary_steps=100,
                log_step_count_steps=100 #CHECK: 具体的输出便捷程度
            )
            # 配置神经网络结构
            estimator = tf.estimator.DNNLinearCombinedRegressor(
                # model directory
                model_dir=self.model_dir,
                # sparse settings
                linear_feature_columns=sparse_fc,
                linear_optimizer=conf.WD_LINEAR_OPTIMIZER,
                # dense settings
                dnn_feature_columns=dense_fc,
                dnn_hidden_units=conf.WD_DENSE_LAYERS,
                dnn_optimizer=tf.train.ProximalAdagradOptimizer(  #NOTE:可以升级为学习率decay形式，见https://www.tensorflow.org/api_docs/python/tf/estimator/DNNLinearCombinedRegressor
                    learning_rate = conf.WD_LEARNING_RATE,
                    l1_regularization_strength=conf.WD_L1_REGULAR_STRENGTH,
                    l2_regularization_strength=conf.WD_L2_REGULAR_STRENGTH),
                config=config
            )
            self.estimator = estimator

    def map_train_data(self, data):
        feature = {}
        for i in range(len(self.colnames)-1):
            feature[self.colnames[i]] = data[i]
        label = tf.cast(data[len(self.colnames)-1], tf.float32)
        return feature, label

    def map_test_data(self, data):
        feature = {}
        for i in range(len(self.colnames)-1):
            feature[self.colnames[i]] = data[i]
        return feature

    def parse_train_instance(self, current_train_data_df, batch_size, train_epochs, is_shuffle=True, buffer_size=10000):
        '''对输入的batch sample转换成送入神经网络训练的数据格式(feature & label)'''
        # 输入的data是一个agent对应数据的dataframe
        dataset = tf.data.Dataset.from_tensor_slices(current_train_data_df.values)
        self.colnames = current_train_data_df.columns.values.tolist()
        dataset = dataset.map(self.map_train_data)
        if is_shuffle:
            dataset = dataset.shuffle(buffer_size = buffer_size)
        dataset = dataset.repeat(train_epochs).batch(batch_size)
        return dataset

    def parse_test_instance(self, current_test_data_df):
        '''对输入的待预测样本（一系列）转换成进行预测的数据格式（仅feature）'''
        test_dataset = tf.data.Dataset.from_tensor_slices(current_test_data_df.values)
        test_dataset = test_dataset.map(self.map_test_data)
        return test_dataset

    def train_input_fn(self): # 包装train input function
        return self.parse_train_instance(self.current_train_data_df,
                                         batch_size=self.batch_size,
                                         train_epochs=self.train_epochs,
                                         is_shuffle=self.is_shuffle,
                                         buffer_size=self.shuffle_buffer_size)
    def test_input_fn(self): # 包装test input function
        return self.parse_test_instance(self.current_test_data_df)

    def _train(self, train_data):
        '''训练模型的核心逻辑'''
        self.current_train_data_df = train_data  # 使训练数据可取到
        try:
            self.estimator.train(input_fn=self.train_input_fn, steps=self.train_verbose_step)
            logging.info("Agent {} network train succeed".format(self.agent_index))
        except Exception as e:
            logging.error("Agent {} network train failed, {}".format(self.agent_index, str(e)))

    def _predict(self, test_data):
        '''给定一批输入，返回对应输出'''
        self.current_test_data_df = test_data # 使测试数据可取到
        pred_y = self.estimator.predict(input_fn=self.test_input_fn)

        #CHECK: 返回的应当是python list格式
        print(pred_y)

        return pred_y
