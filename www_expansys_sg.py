import scrapy

from scrappytutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "expansys"
    allowed_domains = ["www.expansys.com.sg"]
    start_urls = [
        "http://www.expansys.com.sg/"]

    def parse(self, response):
        for href in response.css("ul.asia.me > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

 

    def parse_dir_contents(self, response):


         
        #gfcg
        for sel in response.xpath('//li[@class="title"]//a/@href'):
            url = response.urljoin(sel.extract())
           # print url+' Grid'
            yield scrapy.Request(url, callback=self.parse_grid_contents)
        for href in response.xpath('//a[@class="next"]/@href'):
            url = response.urljoin(href.extract())
            print url+ "next pager"
            yield scrapy.Request(url,callback = self.parse_dir_contents)

    def parse_grid_contents(self,response):
        for r in response.xpath('//html'):
             
            item = DmozItem()
            #print "got in here"
            item['title'] = r.xpath('//h1[@itemprop="name"]/text()').extract()
            item['link'] =  r.xpath('//link/@href')[0].extract()
            item['price'] = r.xpath('//span[@itemprop="price"]/text()').extract()
            item['currency'] = r.xpath('//p[@id="price"]/meta/@content').extract()
            item['sku']=r.xpath('//ul[@class="product-sku"]/li/span/@content').extract()
            #item['desc']=r.xpath('//div[@class="what_we_say"]/text()').extract()
            yield item
            
    def parse_next_page(self,response):
            for sel in response.xpath('//li[@class="title"]//a/@href'):
                url = response.urljoin(sel.extract())
                print url
                yield scrapy.Request(url, callback=self.parse_grid_contents)

            

    
