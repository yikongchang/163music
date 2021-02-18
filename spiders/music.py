import scrapy
from selenium import webdriver
class MusicSpider(scrapy.Spider):
    name = 'music1'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://music.163.com/#/discover/toplist?id=19723756']

    def __init__(self):
        opts = webdriver.ChromeOptions()
        opts.set_headless()
        self.bro = webdriver.Chrome(executable_path='D:\Downloads\chromedriver\chromedriver.exe',options=opts)



    def parse(self, response):
        yun_list = response.xpath('//*[@id="toplist"]/div[1]/div/ul[1]')
        for tree in yun_list:
            up_song_url =0

    def close_spider(self, request):
        self.bro.quit()


