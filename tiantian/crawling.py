# -*- coding: utf-8 -*- 
# @Time     : 2021/3/21
# @Author   : hjhcos
# @File     : crawling.py
# @Project  : crawled
# @Software : PyCharm
# ===================================
import requests
import re
from configparser import ConfigParser
import json


def js_to_json(js: str):

    data = js

    # 对数据的注释进行处理
    pattern = r'(/\*.*?\*/)'
    search = re.findall(pattern, data)
    for s in search:
        data = data.replace(s, '').strip()

    # 对变量声明进行处理
    data = data.replace('var ', '')
    data = '='.join('\n'.join(data.split(';')).split(' = '))
    data = data.replace('%', '%%')

    # 将字符串写入cfg文件
    with open('tian.cfg', 'w', encoding='utf-8') as fd:
        fd.write('[default]\n' + data)

    # 读取cfg数据
    config = ConfigParser()
    config.read('tian.cfg', encoding="utf-8")

    # 将指定数据单独指出
    # 累计收益率、单位净值数据、规模变动
    dataGrandTotal = eval(config['default']['dataGrandTotal'])
    Data_netWorthTrend = eval(config['default']['Data_netWorthTrend'])
    Data_fluctuationScale = eval(config['default']['Data_fluctuationScale'])
    d = {
        'dataGrandTotal': dataGrandTotal,
        'Data_netWorthTrend': Data_netWorthTrend,
        'Data_fluctuationScale': Data_fluctuationScale
    }

    # x 数据 y 数据 type 类别 净资产规模 较上期环比
    categories = d['Data_fluctuationScale']['categories']
    y = [data['y'] for data in d['Data_fluctuationScale']['series']]
    mom = [data['mom'].replace('%', '') for data in d['Data_fluctuationScale']['series']]
    d['Data_fluctuationScale']['series'] = []
    for j in range(len(y)):
        try:
            mom[j] = float(mom[j])
        except:
            mom[j] = round((y[j] - y[j - 1]) / y[j] * 100, 2)
        data = {
            'time': categories[j],
            'y': y[j],
            'mom': mom[j]
        }
        d['Data_fluctuationScale']['series'].append(data)
    d['Data_fluctuationScale'].pop('categories')

    # x 时间 y 数据 equityReturn 权益报酬率 unitMoney unitMoney 每份基金份额折算
    Data_netWorthTrend = d['Data_netWorthTrend']
    # name 三种基金模式 data 日期 收益率 list[set,[set]]
    dataGrandTotal = d['dataGrandTotal']
    name = [data['name'] for data in d['dataGrandTotal']]
    d['dataGrandTotal'] = []
    for i in range(len(name)):
        for j in dataGrandTotal[i]['data']:
            d['dataGrandTotal'].append({
                'name': name[i],
                'date': j[0],
                'earnings': j[1]
            })

    with open('data.json', 'w', encoding='utf-8') as fd:
        fd.write(json.dumps(d))


def get_html(url):
    code = "162412"  # 基金代码
    url = "http://fund.eastmoney.com/pingzhongdata/%s.js" % code
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    
    return requests.get(url, headers=headers)

