#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
import time
from bs4 import BeautifulSoup as bf
from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config
from redisutil import RedisUtil

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('root')

'''
关键词：内存条
搜索条件：1.DDR4 2400
         2.单套容量 8GB
         3.台式机内存
'''
url = 'https://search.jd.com/search?keyword=%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&ev=123_76441%5E5181_76033%5E210_1558%5E'

headers = {
    'Host': 'search.jd.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}


def crwal():
    req = request.Request(url, headers=headers)
    handler = request.BaseHandler()
    opener = request.build_opener(handler)
    response = opener.open(req)
    # logger.info(response.read().decode('utf-8'))
    page = response.read().decode('utf-8')
    soup = bf(page, 'lxml')
    itemlist = soup.select('#J_goodsList > ul > li > div')
    totalprice = 0.0
    pricelist = []
    for item in itemlist:
        priceStr = item.find(class_='p-price').strong.get_text().replace('￥', '')
        price = float(priceStr)
        pricelist.append(price)
        # print(price)
        # print(type(price))
        totalprice = totalprice + price
    pricelist.sort(reverse=True)
    averageprice = totalprice / len(itemlist)
    print(averageprice)
    # priceString = unicode(nString)
    r = RedisUtil.getredis()

    param = {
        'date': time.strftime('%Y-%m-%d', time.localtime()),
        'price': averageprice,
        'itemlist': pricelist
    }

    r.lpush('JDPrice', param)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(crwal, 'cron', day_of_week='*', hour='13', minute='30')
    scheduler.start()
    try:
        while True:
            time.sleep(2)
            print('sleep')
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

        print('Exit The Job')
