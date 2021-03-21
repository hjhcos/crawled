# -*- coding: utf-8 -*- 
# @Time     : 2021/3/21
# @Author   : hjhcos
# @File     : dataprocess.py
# @Project  : crawled
# @Software : PyCharm
# ===================================
"""
获取所有商品
"""
import json


def set_auctions(auctions):
	"""设置商品信息"""
	__auctions = ['auctions', ('store', 'name', 'price', 'location', 'sales', 'comments'), []]
	for i in range(len(auctions)):
		for j in range(len(auctions[i])):
			temp = (
				auctions[i][j]['nick'],
				auctions[i][j]['raw_title'],
				auctions[i][j]['view_price'],
				auctions[i][j]['item_loc'],
				auctions[i][j]['view_sales'].replace('人付款', '') if 'view_sales' in auctions[i][j] and (not auctions[i][j]['view_sales'] is '') else 0,
				auctions[i][j]['comment_count'] if not auctions[i][j]['comment_count'] is '' else 0,
			)
			__auctions[2].append(temp)

	print(__auctions)


def set_filter(nav):
	"""设置过滤参数 """
	# 不能用key 会报错
	__common = ['filter', ('text', 'name', 'keyword', 'value'), []]
	for common in nav:
		for text in common:
			for sub in text['sub']:
				temp = (
					text['text'],
					sub['text'],
					sub['key'],
					sub['value'],
				)
				__common[2].append(temp)
	print(__common[2])


def get_filter():
	"""获取过滤参数"""
	title = mysql.server.select_distinct('text', 'filter')
	d = {}
	for head in title:
		key = mysql.server.select(column='keyword', table='filter', filtrate=True, condition="text = '%s'" % head[0])
		value = mysql.server.select(column='name, value', table='filter', filtrate=True, condition="text = '%s'" % head[0])
		d[head[0]] = [key[0][0]] + [value]
	return title, d


def get_auctions():
	"""获取商品参数"""
	stores = mysql.server.select_distinct('store', 'auctions')
	d = {}
	for store in stores:
		d[store[0]] = mysql.server.select(column='*', table='auctions', filtrate=True, condition="store = '%s'" % store[0])


if __name__ == '__main__':
	with open("data.json", "r", encoding="utf-8") as fd:
		data = json.load(fd)
	# auction = getAuctions([d['mods']['itemlist']['data']['auctions'] for d in data])
	print(get_filter())		# ([('品牌',), ('尺码',), ('适用年龄',), ('女装',)], {'品牌': ['ppath', [('20000:8598007',),
	# writeDatabase(*auction, mode='w')
	# writeDatabase(*filters, mode='w')
	# a = readDatabase('auctions')
	# b = readDatabase('filter')
	# print(getAuctions())
	pass
