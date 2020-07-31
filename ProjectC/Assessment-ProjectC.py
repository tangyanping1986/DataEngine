# 使用KMeans进行聚类分析
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np

def main():
    # 数据加载
    data = pd.read_csv('E:\Python/数据分析训练营-结营考试/数据分析训练营-结营考试/ProjectC/CarPrice_Assignment.csv')
    train_x = data[["car_ID","symboling","CarName", "fueltype", "aspiration", "doornumber",
                    "carbody", "drivewheel", "enginelocation", "wheelbase", "carlength","carwidth",
                    "carheight", "curbweight", "enginetype", "cylindernumber", "enginesize","fuelsystem",
                    "boreratio", "stroke", "compressionratio", "horsepower", "peakrpm","citympg",
                    "highwaympg", "price"]]
    print(train_x.shape)

    # 存在非数值类型，需要使用LaberlEncoder,将非数值字段转化为数值
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    columns=['CarName','fueltype','aspiration','doornumber','carbody','drivewheel','enginelocation','enginetype','cylindernumber','fuelsystem']
    for column in columns:
        train_x[column] = le.fit_transform(train_x[column])

    # 规范化到 [0,1] 空间
    min_max_scaler=preprocessing.MinMaxScaler()
    train_x=min_max_scaler.fit_transform(train_x)
    pd.DataFrame(train_x).to_csv('temp.csv', index=False)
    print(train_x)

    ### 使用KMeans聚类
    kmeans = KMeans(n_clusters=7)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    # 合并聚类结果，插入到原数据中
    result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
    result.rename({0:u'聚类结果'},axis=1,inplace=True)
    print(result)
    # 将结果导出到CSV文件中
    result.to_csv("customer_cluster_result.csv",index=False)



    # K-Means 手肘法：统计不同K取值的误差平方和
    import matplotlib.pyplot as plt
    sse = []
    for k in range(1, 11):
        # kmeans算法
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_x)
        # 计算inertia簇内误差平方和
        sse.append(kmeans.inertia_)
    x = range(1, 11)
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(x, sse, 'o-')
    plt.show()

    '''
    ### 使用层次聚类
    from scipy.cluster.hierarchy import dendrogram, ward
    from sklearn.cluster import KMeans, AgglomerativeClustering
    import matplotlib.pyplot as plt
    model = AgglomerativeClustering(linkage='ward', n_clusters=3)
    y = model.fit_predict(train_x)
    print(y)

    linkage_matrix = ward(train_x)
    dendrogram(linkage_matrix)
    plt.show()
    '''

if __name__ == '__main__':
    main()

