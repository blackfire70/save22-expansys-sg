import scrapy
import datetime
from expansys_sg.items import ExpansysItem
import re

#init
class ExpansysSpider(scrapy.Spider):
    name = "expansys"
    allowed_domains = ["www.expansys.com.sg"]
    start_urls = [
       "http://www.expansys.com.sg/mobile-phones/phone-accessories/","http://www.expansys.com.sg/tablet-pcs+ipads/tablet-accessories/","http://www.expansys.com.sg/action/cameras/compact-camera-accessories/","http://www.expansys.com.sg/computing/computer-hardware+accessories/"]

    def parse(self, response):
        for ur in self.start_urls:
            yield scrapy.Request(ur, callback=self.parse_dir_contents)

        for href in response.css("ul.asia.me > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

 

    def parse_dir_contents(self, response):


         
        #gfcg
        for sel in response.xpath('//li[@class="title"]//a/@href'):
            url = response.urljoin(sel.extract())
            
            yield scrapy.Request(url, callback=self.parse_grid_contents)
        for href in response.xpath('//a[@class="next"]/@href'):
            url = response.urljoin(href.extract())
            print url+ "next pager"
            yield scrapy.Request(url,callback = self.parse_dir_contents)
    lnkk=[]
    def parse_grid_contents(self,response):
        for r in response.xpath('//html'):
             
            item = ExpansysItem()
            #print "got in here"
            if r.xpath('//link/@href')[0].extract() not in self.lnkk:
                item['title'] = r.xpath('//h1[@itemprop="name"]/text()').extract()
                item['link'] =  r.xpath('//link/@href')[0].extract()
                
                if not r.xpath('//li[@class="instock"]')  and not  r.xpath('//li[@class="infostock"]'):
                    item['price'] = r.xpath('//p[@id="price"]/strong/text()').extract()
                    
                else:
                    item['price'] = r.xpath('//span[@itemprop="price"]/text()').extract()
                item['currency'] = r.xpath('//p[@id="price"]/meta/@content').extract()
                m = re.search(r'sku:(\d+)',r.xpath('//ul[@class="product-sku"]/li/span/@content')[0].extract())
                item['sku']=m.group(0)
                n = re.search(r'ean:(\d+)',r.xpath('//ul[@class="product-sku"]/li/span/@content')[1].extract())
                if n:
                    item['ean'] = n.group(0)
                item['primary_image_url']=r.xpath('//a[@class ="js-primary-image-link"]/@href').extract()
                item['time'] = datetime.datetime.now().time()
                self.lnkk.append(r.xpath('//link/@href')[0].extract())
            
            item['category'] =r.xpath('//ul[@id="breadcrumbs"]//span/text()').extract()
            #item['desc']=r.xpath('//div[@class="what_we_say"]/text()').extract()
            yield item
            
    def parse_next_page(self,response):
            for sel in response.xpath('//li[@class="title"]//a/@href'):
                url = response.urljoin(sel.extract())
                print url
                yield scrapy.Request(url, callback=self.parse_grid_contents)

            

    
