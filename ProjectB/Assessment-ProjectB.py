import pandas as pd
import time

# 数据加载
data = pd.read_csv('E:\Python/数据分析训练营-结营考试/数据分析训练营-结营考试/ProjectB/订单表.csv', encoding='gbk')
#对客户ID进行排序
df= data.sort_values('客户ID', ascending=False)

def main():
    # 采用efficient_apriori工具包
    def rule1():
        from efficient_apriori import apriori
        start = time.time()
        # 得到一维数组orders_series，并且将客户ID作为index, 产品名称为Item取值
        orders_series = df.set_index('客户ID')['产品名称']
        # 将数据集进行格式转换
        transactions = []
        temp_index = 0
        for i, v in orders_series.items():
            if i != temp_index:
                temp_set = set()
                temp_index = i
                temp_set.add(v)
                transactions.append(temp_set)
            else:
                temp_set.add(v)

        # 挖掘频繁项集和频繁规则
        itemsets, rules = apriori(transactions, min_support=0.02, min_confidence=0.5)
        print('频繁项集：', itemsets)
        print('关联规则：', rules)
        end = time.time()
        print("用时：", end - start)

    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    # 采用mlxtend.frequent_patterns工具包
    def rule2():
        from mlxtend.frequent_patterns import apriori
        from mlxtend.frequent_patterns import association_rules
        pd.options.display.max_columns = 100
        start = time.time()
        hot_encoded_df = df.groupby(['客户ID', '产品名称'])['产品名称'].count().unstack().reset_index().fillna(0).set_index(
            '客户ID')
        hot_encoded_df = hot_encoded_df.applymap(encode_units)
        frequent_itemsets = apriori(hot_encoded_df, min_support=0.02, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.5)
        print("频繁项集：", frequent_itemsets)
        print("关联规则：", rules[(rules['lift'] >= 1) & (rules['confidence'] >= 0.5)])
        # print(rules['confidence'])
        end = time.time()
        print("用时：", end - start)


    rule1()
    print('-' * 100)
    #rule2()

if __name__ == '__main__':
    main()
