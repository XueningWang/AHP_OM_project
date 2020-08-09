#coding:utf-8
import pandas as pd
import tensorflow as tf

a = {"a": 2, "b": 4, "c": 5}
b = {"a": 1, "b": 7, "c": 10}
a_df = pd.DataFrame([a, b])
print(a_df.to_dict(orient="list"))

a = {"a": 2.5, "b": 4, "c": 5}
b = {"a": 1.9, "b": 7, "c": 10}
df = pd.DataFrame([a, b])
print(df)
print(df.to_dict(orient="list"))

dataset = tf.data.Dataset.from_tensor_slices(df.values)
for dt in dataset.take(5):
    print(dt)

def map(data):
    return data[1]
dataset = dataset.map(map)
for dt in dataset.take(3):
    print(dt)
# 结论：tensor可以通过索引拿到

a = {}
a['q'] = 9, 10
print(a)
