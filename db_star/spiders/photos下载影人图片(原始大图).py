# -*- coding: utf-8 -*-
import scrapy,os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PhotosSpider(CrawlSpider):

    name = 'photos'
    num = input("input number:")
    path = "img//%s" % num
    if not os.path.exists(path):
        os.makedirs(path)
    allowed_domains = ["movie.douban.com", "img1.doubanio.com", "img2.doubanio.com",
                       "img3.doubanio.com", "img4.doubanio.com","img9.doubanio.com"]
    start_urls = ['http://movie.douban.com/celebrity/%s/photos/'% num]

    photo_links = LinkExtractor(allow="photo", tags="img", attrs="src", deny_extensions="")
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        'referer': 'http://movie.douban.com/celebrity/%s/photos/'% num
    }
    rules = (
        Rule(LinkExtractor(allow="sortby=like")),
        Rule(photo_links, process_links="parse_links", process_request='request_photos', callback='parse_photos')
    )


    def parse_links(self, links):
        for link in links:
            link.url = link.url.replace("/m/", "/raw/").replace("webp", "jpg")
        return links

    def parse_photos(self, response):
        photo_name = response.url.split("/")[-1]
        with open(self.path + "//" + photo_name, "wb") as f:
            f.write(response.body)

    def request_photos(self, request):
        photo_name = request.url.split("/")[-1]
        self.headers['referer'] += photo_name[1:] + '/'
        newRequest = request.replace(headers=self.headers)
        newRequest.meta.update(cookiejar=1)
        return newRequest