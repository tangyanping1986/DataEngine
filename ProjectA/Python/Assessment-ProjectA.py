import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_page_content(url):
    # 请求URL
    url = 'http://car.bitauto.com/xuanchegongju/?mid=8'
    # 得到页面的内容
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(url,headers=headers,timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def analysis(soup):
    # 找到完整的价格搜索结果
    temp = soup.find('div', class_="search-result-wrapper")
    # 创建DataFrame
    df = pd.DataFrame(columns = ['名称', '最低价格', '最高价格', '产品图片链接'])
    tr_list = temp.find_all('div', class_='search-result-list-item')
    for tr in tr_list:
        img = tr.find('img')['src'] # 提取图片链接
        name = tr.find('p', class_="cx-name text-hover").string # 提取车型名称
        # 提取价格范围
        price = tr.find('p', class_="cx-price").string
        if price == '暂无':
          cheapest_price = -1
          highest_price = -1
        else:
          cheapest_price = float(price.split('-')[0])
          highest_price = float(price.split('-')[1][:-1])

        new = {'名称': name, '最低价格': cheapest_price,
                    '最高价格': highest_price, '产品图片链接': img}
        df = df.append(new, ignore_index=True)
    return df

url = 'http://car.bitauto.com/xuanchegongju/?mid=8'
page_num = 3  # 获取信息的页数
# 创建循环DataFrame
result = pd.DataFrame(columns=['名称', '最低价格', '最高价格', '产品图片链接'])
for i in range(page_num):
    url = url + str(i + 1) + '.shtml'
    soup = get_page_content(url)
    df = analysis(soup)
    print(df)
    result = result.append(df)

# 提取结果保存为csv文件
df.to_csv('projectA_result.csv', index=False)