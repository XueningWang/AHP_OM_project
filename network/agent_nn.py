#coding: utf-8

import tensorflow

class AgentDeepNetwork:
    def __init__(self, conf):
        self.network_params = conf.NETWORK_PARAMS
        self.agent_network = 0#直接做成一个tf神经网络的类，在network_init里面初始化

    def network_init(self):
        '''按照配置，构建一个神经网络结构'''

    def process_batch_sample(self):
        '''对输入的batch sample转换成送入神经网络训练的数据格式'''
        #继续开发SAMPLE格式！

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
        #继续开发输出格式！
