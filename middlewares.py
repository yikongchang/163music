# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from time import sleep
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random




class WangyiyunDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # bro = spider.bro
        # bro.get(spider.start_urls[0])
        # iframe = bro.find_element_by_tag_name("iframe")
        # bro.switch_to.frame(iframe)
        # body = bro.page_source
        # return HtmlResponse(url=spider.start_urls[0],body=body,encoding='utf-8',request=request )
        # UA池
        user_agent = random.choice(spider.settings['USER_AGENT_LIST'])
        request.headers['User-Agent'] = user_agent
        return None

    def process_response(self, request, response, spider):

        # 拦截响应，处理页面动态加载和 iframe 嵌套
        bro = spider.bro
        all_link =['https://music.163.com/#/discover/toplist?id=19723756']
        temp = spider.link.extract_links(response)
        for i in temp:
            all_link.append(i.url)
        if request.url in all_link:
            bro.get(request.url)
            iframe = bro.find_element_by_tag_name("iframe")
            bro.switch_to.frame(iframe)
            page_text = bro.page_source
            new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
            return new_response
        else:
            return response


    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
