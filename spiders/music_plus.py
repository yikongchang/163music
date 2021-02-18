# encoding: utf-8
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from time import sleep
from ..items import WangyiyunItem
import pymysql

class MusicSpider(CrawlSpider):
    # 初始化selenium浏览器对象
    def __init__(self):
        super(MusicSpider,self).__init__( )
        opts = webdriver.ChromeOptions()
        opts.set_headless()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.bro = webdriver.Chrome(executable_path='D:\Downloads\chromedriver\chromedriver.exe', options=opts)

    name = 'music'
    # allowed_domains = ['www.xxx.com']
    # 全站爬取规则
    start_urls = ['https://music.163.com/#/discover/toplist?id=19723756']
    link =LinkExtractor(allow=r'\/discover\/toplist\?id=\d+')

    rules = (
        Rule(link, callback='parse_item', follow=False),
    )

    all_link = []
    # 增量式爬取，提交管道前先检索数据库是否数据已存在
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root',db='wy_music')
    cur = conn.cursor()

    def parse_item(self, response):
        #http://music.163.com/song/media/outer/url?

        info = response.xpath('//tbody')
        for tree in info:
            name = tree.xpath('//tr//span[@class="txt"]//b/@title').extract()
            url = tree.xpath('//tr//span[@class="txt"]/a/@href').extract()
            singer = tree.xpath('//td[4]/div/@title').extract()
            for j in range(len(name)):
                item = WangyiyunItem()
                song_name = ''.join(name[j])
                song_url ='http://music.163.com/song/media/outer/url?'+url[j].split('?')[1]
                song_singer = ''.join(singer[j])

                item['name']=song_name
                item['url']=song_url
                item['singer']=song_singer
                sql='select 1 from music where song_url=%s'
                val=song_url
                if self.cur.execute(sql,val)==0:
                    yield item
                else:
                    print('数据已存在，本次不提交管道')




