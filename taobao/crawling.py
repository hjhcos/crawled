# -*- coding: utf-8 -*- 
# @Time     : 2021/3/21
# @Author   : hjhcos
# @File     : crawling.py
# @Project  : crawled
# @Software : PyCharm
# ===================================
from requests_html import HTMLSession
import json
from time import sleep
import dataprocess

# 商品搜索引擎值
article_postfix = {
    "q": None,  # 搜索内容
    "imgfile": None,
    "js": "1",
    "stats_click": [  # 按钮点击状态与tab搭配
        "search_radio_all:1",  # 所有 (默认)
        "search_radio_tmall:1",  # 天猫
        "search_radio_old:1",  # 二手
    ], "initiative": None,  # 初始值 staobaoz_20201106
    "tab": [  # 搜索内容标签与stats_click搭配
        "all",  # 所有(默认)
        "mall",  # 天猫
        "old",  # 二手
    ], "ie": "utf-8",  # 编码格式
    "cps": None,  # 是否开启筛选
    "ppath": None,  # 筛选条件
    "sort": [  # 商品排序
        "default",  # 综合
        "sale-desc",  # 销量
        "credit-desc",  # 信用
        "price-asc",  # 价格(从低到高)
        "price-desc",  # 价格(从高到低)
        "total-asc",  # 总价(从低到高)
        "total-desc",  # 总价(从高到低)
    ], "filter": None,  # 价格受喜率
    "s": None  # 页码 [0~100] 44
}

# 店铺搜索引擎值
store_postfix = {
    "q": None,  # 搜索内容
    "imgfile": None,
    "js": "1",
    "stats_click": [  # 按钮点击状态与tab搭配
        "search_radio_all:1",  # 所有 (默认)
        "search_radio_tmall:1",  # 天猫
        "search_radio_old:1",  # 二手
    ], "initiative": None,  # 初始值 staobaoz_20201106
    "ie": "utf-8",  # 编码格式
    "cps": None,  # 是否开启筛选
    "ppath": None,  # 筛选条件
    "sort": [  # 商品排序
        "default",  # 综合
        "sale-desc",  # 销量
        "credit-desc",  # 信用
    ],
    # 店铺类型: isb shop_type ratesum
    "isb": [  # 店铺来源
        None,  # 不限  全球购
        "0",  # 淘宝店
        "1",  # 天猫店
    ],
    "shop_type": [  # 全球购专属参数
        None,  # 淘宝店 天猫 不限
        "2",  # 全球购
    ],
    "ratesum": [  # 淘宝店专属参数
        None,  # 天猫 全球购 不限
        "jin",  # 金冠店
        "huang",  # 皇冠店
        "zhuan",  # 钻级店
        "xin"  # 心级店
    ],
    "goodrate": [  # 好评率 只要isb=0时可用 天猫附加参数 会给 isb 赋值 0
        None,  # 天猫
        # 以下参数 适用 淘宝 不限 全球购
        "10000,10010",
        "9900%,",
        "9800%,",
        "9700%,",
        "9600%,",
    ],
    "loc": [],  # 地点 多个地点可以用逗号隔开
    "s": None  # 页码 [0~100] 20
}

location = [
    "北京 上海 广州 深圳 杭州 江浙泸 珠三角 港澳台 江浙泸皖 长沙 长春 成都 重庆 大连 东莞 佛山 福州 "
    "贵阳 合肥 金华 济南 嘉兴 昆明 宁波 南昌 南京 青岛 泉州 沈阳 苏州 天津 温州 无锡 武汉 西安 厦门 "
    "郑州 中山 石家庄 哈尔滨 安徽 福建 甘肃 广东 广西 贵州 海南 河北 河南 湖北 湖南 江苏 江西 吉林 "
    "辽宁 宁夏 青海 山东 山西 陕西 云南 四川 西藏 新疆 浙江 澳门 香港 台湾 内蒙古 黑龙江"
]


class Engine:

    def __init__(self, **kwargs):
        self.q = None
        self.s = None
        self.cps = None
        self.cat = None
        self.ppath = None
        self.loc = None
        self.mode = None
        self.kwargs = None
        self.json = None
        self.url = None  # 网站url(必需)
        self.cookie = None  # 验证登入(必需)
        self.filter = None
        self.session = HTMLSession()
        self.article = "https://s.taobao.com/search?"  # 商品url
        self.store = "https://shopsearch.taobao.com/search?"  # 店铺url
        self.header = {
            "cookie": None,
        }

    def get_cookie(self, user, password):
        """获取cookie"""
        url = 'https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0'
        parameter = {
            'loginId': user,
            'password2': password,
        }
        html = self.session.post(url, data=parameter)
        print(html.cookies)
        self.header['cookie'] = html.cookies

    def __get_parameter(self, s):
        """获取参数"""
        self.kwargs = {
            'q': self.q,
        }
        if self.mode == '宝贝':
            self.url = self.article
        else:
            self.url = self.store
        if self.cps == 'yes':
            self.kwargs['cps'] = 'yes'
            if self.cat:
                self.kwargs['cat'] = self.cat
            else:
                self.kwargs['ppath'] = self.ppath
            if self.loc:
                self.kwargs['loc'] = self.loc
        if s == 0:
            pass
        else:
            self.kwargs['s'] = s * 44
        return self.kwargs

    def __get_html(self, s):
        """获取网页内容并解码 """
        self.__get_parameter(s)
        html = self.session.get(self.url, headers=self.header, params=self.kwargs)
        print(html.url)
        html = html.text
        start = html.find('g_page_config = ') + len('g_page_config = ')
        end = html.find('"shopcardOff":true}') + len('"shopcardOff":true}')
        # with open('index.html', 'w', encoding='utf-8') as f:
        # 	f.write(html)
        js = json.loads(html[start:end + 1])
        self.json.append(js)
        sleep(1)

    def load_data(self):
        """ 获取搜索数据 搜索结果写到json文件里面 """
        self.json = []
        for s in range(int(self.s)):
            self.__get_html(s)
        self.set_auctions()

    # self.set_filter()

    def set_ppath(self, ppath):
        """设置ppath值 : ;"""
        self.cps = 'yes'
        self.ppath = ppath.replace(":", "%3A").replace(";", "%3B")

    def set_loc(self, loc):
        """设置loc值 ,"""
        self.cps = 'yes'
        self.ppath = self.ppath if self.ppath else ''
        self.loc = loc.replace(",", "%2C")

    def set_auctions(self):
        """ 设置网站所有商品信息 list """
        return dataprocess.set_auctions([d['mods']["itemlist"]["data"]["auctions"] for d in self.json])

    def set_filter(self):
        """ 设置所有宝贝分类 dict {common(所有分类别) adv(筛选条件)}"""
        return dataprocess.set_filter([self.json[0]['mods']["nav"]['data']['common']])

    @staticmethod
    def get_filter():
        """get filter"""
        # return dataprocess.getFilter()
        ...

    def get_pager(self):
        """ 获取 s 页码"""
        return [d['mods']['pager']['data'] for d in self.json]

    def get_price(self):
        """获取受喜率 价格区间 list """
        return self.json[0]['mods']['sortbar']['data']['price']['rank']

    def get_related(self):
        """ 获取相关搜索 list """
        return self.json[0]["related"]["data"]["words"]

    def get_tab(self):
        """ 获取tab参数 list"""
        return self.json[0]["tab"]["data"]["tabs"]

    def get_header(self):
        """ 获取url参数 dict
            q			关键字
            tabParams	后缀
                js
                stats_click
                initiative_id
                ie
            dropdown	切换前缀  list
                url
                text
        """
        return self.json[0]["header"]["data"]

    def detection(self):
        ...


if __name__ == '__main__':
    engine = Engine()
    # engine.url = engine.article
    engine.mode = '宝贝'
    # engine.q = '树莓派'
    engine.s = 3
    # engine.header["cookie"] = engine.cookie
    # engine.loadData()
    # with open('data.json', 'w', encoding='utf-8') as fd:
    # 	json.dump(engine.json, fd)
    # with open('data.json', 'r', encoding='utf-8') as fd:
    # 	engine.json = json.load(fd)
    # with open('a.json', 'w', encoding='gbk') as fd:
    # 	json.dump(engine.getAuctions(), fd)
    # print(engine.getAuctions())
    # title, data = engine.get_filter()
    # print(title)
    # print(data)
    # print(engine.getPrice())
    # engine.get_cookie(user=u, password=telephone)
    engine.load_data()
