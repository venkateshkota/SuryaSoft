# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import Request

class DevAppleSpider(scrapy.Spider):
    name = "dev_apple"

    def __init__(self, *args, **kwargs):
        super(DevAppleSpider, self).__init__(*args, **kwargs)
        self.final_data = {}
        self.session_data = []
        
    allowed_domains = ["developer.apple.com"]
    start_urls = []
    url = 'https://developer.apple.com/videos/wwdc'
    years_list =["2012","2013","2014","2015","2016"]
    
    for year in years_list:
        start_urls.append(url + year)

    def parse(self, response):
        sel = Selector(response)
        count = 0
        data = 'normal'
        videos_list = sel.xpath('//section[@class="row"]//a/@href').extract()
        for video in videos_list:
            count = count + 1
            if count == len(videos_list) - 1:
                data = 'last_url'
            url = 'https://developer.apple.com' + video
            yield Request(url,callback=self.parse_next,meta={'var':data})

    def parse_next(self, response):
        sel = Selector(response)
        status = response.meta['var']
        print status
        if status == 'normal':
            title = str(''.join(sel.xpath('//h1/text()').extract()))
            year_session =  str(''.join(response.xpath('//p[@class="smaller lighter"]/text()').extract()))
            year = year_session.split(' - ')[0]
            session = year_session.split(' - ')[1]
            year_final = ''.join(re.findall('\d+',year))
            session_final = ''.join(re.findall('\d+',session))
            hd = sel.xpath('//li[@class="video"]//ul//li')[0]
            sd = sel.xpath('//li[@class="video"]//ul//li')[1]
            hd_final = str(''.join(hd.xpath('.//a/@href').extract()))
            sd_final = str(''.join(sd.xpath('.//a/@href').extract()))
            presentation_slide = str(''.join(sel.xpath('//li[@class="document"]//@href').extract()))
            data = {
            'title': title,
            'year': year_final,
            'sessionNumber': session_final,
            'hdVideo': hd_final,
            'sdVideo': sd_final
            }
            self.session_data.append(data)
        if status == 'last_url':
            self.final_data['sessions'] = self.session_data
            print self.final_data
