import pandas as pd
#数据加载
train = pd.read_csv('E:\Python/Data_Engine_with_Python-master20200715/Data_Engine_with_Python-master/L6/jetrail/train.csv')

def main():

    print(train.head())
    #转换为pandas中的日期格式
    train['Datetime'] = pd.to_datetime(train.Datetime, format='%d-%m-%Y %H:%M')
    #将Datatime作为train的索引
    train.index = train.Datetime
    print(train.head())

    #去掉ID，Datetime字段
    train.drop(['ID', 'Datetime'], axis=1, inplace=True)
    print(train.head())

    #按照天进行采集
    daily_train = train.resample('D').sum()
    print(daily_train.head())
    daily_train['ds'] = daily_train.index
    daily_train['y'] = daily_train.Count
    daily_train.drop(['Count'], axis=1, inplace=True)
    print(daily_train.head())

    from fbprophet import Prophet
    #拟合proph模型
    m = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1)
    m.fit(daily_train)
    #预测未来7个月，213天
    future = m.make_future_dataframe(periods=213)
    forecast = m.predict(future)
    print(forecast)

    m.plot(forecast)
    m.plot_components(forecast)

if __name__ == '__main__':
    main()
