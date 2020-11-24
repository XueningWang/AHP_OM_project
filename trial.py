#coding:utf-8

# a = {"a": 2, "b": 4, "c": 5}
# b = {"a": 1, "b": 7, "c": 10}
# a_df = pd.DataFrame([a, b])
# print(a_df.to_dict(orient="list"))
#
# a = {"a": 2.5, "b": 4, "c": 5}
# b = {"a": 1.9, "b": 7, "c": 10}
# df = pd.DataFrame([a, b])
# print(df)
# print(df.to_dict(orient="list"))
#
# dataset = tf.data.Dataset.from_tensor_slices(df.values)
# for dt in dataset.take(5):
#     print(dt)
#
# def map(data):
#     return data[1]
# dataset = dataset.map(map)
# for dt in dataset.take(3):
#     print(dt)
# # 结论：tensor可以通过索引拿到
#
# a = {}
# a['q'] = 9, 10
# print(a)
#
# # 尝试索引数据类型
# a = {}
# a[1] = 0
# print(a)
# # 结论：字典可以用int型作为索引
#
# # 尝试itertools笛卡尔积
# import itertools
# feasible_actions = [[1, 0, 2], [2, 9, 2]]
# p_res = itertools.product(*feasible_actions)
# for ele in p_res:
#     print(ele)

# 尝试list reshape
# a = [0,1,3,4,23,43,23,3]
# b = a.reshape(4,2)
# print(b)
# 结论：list不能reshape

# # 尝试randrange
# import random
# random_index = random.randrange(0,10)
# print(random_index)

# # 10.19 DEBUG数据格式转换
import conf
from utils_global import *
agents = conf.AGENT_COMPONENTS
# revert_res = revert_agent_comp_mapping(agents)
# print(revert_res)

# 10.26 DEBUG基础信息构建
sys_comp_info = conf.SYSTEM_COMPONENT
sys_comp_info, comp_agent_mapping, flatten_colname_list, flatten_colname_list_agents = construct_comp_info(sys_comp_info, agents)
print("Done")
