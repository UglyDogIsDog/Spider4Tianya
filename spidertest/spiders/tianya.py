from scrapy import Request
from scrapy.spiders import Spider
from spidertest.items import FirstItem, SecondItem
from inline_requests import inline_requests


class Tianya(Spider):
    name = 'tianya'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    start_urls = ['http://bbs.tianya.cn/list-develop-1.shtml']

    @inline_requests
    def parse(self, response):
        final_buttom = response.xpath('//div[@class="short-pages-2 clearfix"]/div/a/text()').extract()[-1]
        list_page = response
        while final_buttom == "下一页":
            url_list = list_page.xpath('//td[@class="td-title faceblue"]/a/@href').extract()
            print(url_list)
            for url in url_list:
                blog_url = 'http://bbs.tianya.cn' + url
                first_page = yield Request(blog_url)

                first_item = FirstItem()
                title = first_page.xpath('//span[@class="s_title"]/span/text()').extract()
                if title and title[0].strip():
                    first_item['title'] = title[0].strip()
                else:
                    first_item['title'] = ""
                print(first_item['title'])
                print(blog_url)
                passage = first_page.xpath('//div[@class="bbs-content clearfix"]').xpath('string(.)').extract()
                if passage and passage[0].strip():
                    first_item['passage'] = passage[0].strip()
                else:
                    first_item['passage'] = ""
                first_item['response'] = []

                next_page = first_page
                while True:
                    first_item['response'] += [sen.strip() for sen in
                                               next_page.xpath('//div[@class="bbs-content"]').xpath('string(.)').extract() if sen.strip()]
                    if not next_page.xpath('//a[@class="js-keyboard-next"]/@href').extract(): # no choice for next page
                        break
                    next_url = "http://bbs.tianya.cn" + next_page.xpath('//a[@class="js-keyboard-next"]/@href').extract()[0]
                    next_page = yield Request(next_url)

                yield first_item
            final_buttom = list_page.xpath('//div[@class="short-pages-2 clearfix"]/div/a/text()').extract()[-1]
            next_url = "http://bbs.tianya.cn" + list_page.xpath('//div[@class="short-pages-2 clearfix"]/div/a/@href').extract()[-1]
            print(next_url)
            list_page = yield Request(next_url) #next page