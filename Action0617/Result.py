import requests
from bs4 import BeautifulSoup
import pandas as pd

# 请求URL
def get_page_content(url):
    #得到页面内容
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(url, headers=headers, timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser')
    return soup

# 分析当前页面内容
def analysis(soup):
    # 找到具备完整投诉信息的类
    temp = soup.find('div', class_='tslb_b')
    # 创建DataFrame,对要爬取数据的各字段进行命名
    df = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        # 提取汽车各项投诉信息,解析各字段，放入DataFrame中
        temp= {}
        td_list = tr.find_all('td')
        if len(td_list) > 0:
            #解析各个字段的内容
            id, brand, car_model, type, desc, problem, datetime, status = \
                td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            temp["id"], temp["brand"], temp["car_model"], temp["type"], temp["desc"], temp["problem"], temp["datetime"], temp["status"] = id, brand, car_model, type, desc, problem, datetime, status
            df = df.append(temp, ignore_index=True)
    return df

page_num = 18  # 获取信息的页数
basic_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'  # 网页链接

# 创建循环DataFrame
result = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
for i in range(page_num):
    url = basic_url + str(i + 1) + '.shtml'
    soup = get_page_content(url)
    df = analysis(soup)
    print(df)
    result = result.append(df)
# 提取结果保存为csv文件
result.to_csv('result.csv', index=False)