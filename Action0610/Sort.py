from pandas import Series, DataFrame
data = {'张飞': [68, 65, 30], '关羽': [95, 76, 98], '刘备': [98, 86, 88], '典韦': [90, 88, 77], '许褚': [80, 90, 90]}
df = DataFrame(data, index=['语文', '数学', '英语'], columns=['张飞', '关羽', '刘备', '典韦', '许褚'])
print("平均成绩")#平均值
print(df.mean())#平均值
print("最小成绩")#平均值
print(df.min())#最小值
print("最大成绩")#平均值
print(df.max())#最大值
print("成绩方差")#平均值
print(df.var())#方差
print("成绩标准差")#平均值
print(df.std())#标准差

#总成绩及排序
print("总成绩排序")#平均值
data_sum=df.sum(axis=0)
print(data_sum.sort_values(ascending=False))
