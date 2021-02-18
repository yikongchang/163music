# encoding:utf-8


import os
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request


class WangyiyunPipeline:

    path ='./music'
    # 函数只执行一次

    def open_spider(self, spider):
        print('Begin')
        if not os.path.exists(path=self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        name =item['name']
        url = item['url']
        sql = 'insert into music (song_name,song_url)values(%s,%s)'
        val = (name, url)
        spider.cur.execute(sql, val)
        spider.conn.commit()

        return item


class DownloadMusic(FilesPipeline):

    def get_media_requests(self, item, info):

        yield Request(item['url'], [])

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        file_name = item['name']+'-'+item['singer']+'.mp3'
        return file_name

    def item_completed(self, results, item, info):
        return item

    # 最后执行完爬虫，释放所以资源
    def close_spider(self, spider):
        spider.bro.quit()
        spider.conn.close()
        spider.cur.close()
        print('end')