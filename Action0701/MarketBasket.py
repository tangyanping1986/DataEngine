import pandas as pd
import numpy as np
from efficient_apriori import apriori

#Header=None，第一行不将作为head
dataset = pd.read_csv('E:\Python/Data_Engine_with_Python-master/Data_Engine_with_Python-master/L4/MarketBasket/Market_Basket_Optimisation.csv',header=None)
print(dataset.shape)

#将数据放到transactions里
transacations = []
for i in  range(0, dataset.shape[0]):
    temp = []
    for j in  range(0,20):
        if str(dataset.values[i,j]) !='nan':
            temp.append(str(dataset.values[i,j]))
    transacations.append(temp)

#挖掘频繁项集与关联规则
itemsets,rules = apriori(transacations, min_support=0.05, min_confidence=0.2)
print('频繁项集:', itemsets)
print('关联规则:', rules)
