import scrapy
from scrapy.spider import CrawlSpider,Rule
import datetime
import re
from scrapy.linkextractors import LinkExtractor
from expansyscrawl.items import ExpansyscrawlItem
class Expansys(CrawlSpider):
    name =  'expansys'
    now = datetime.datetime.now()
    allowed_domains =['expansys.com.sg']
    start_urls = ["http://www.expansys.com.sg/","http://www.expansys.com.sg/mobile-phones/phone-accessories/","http://www.expansys.com.sg/tablet-pcs+ipads/tablet-accessories/","http://www.expansys.com.sg/action/cameras/compact-camera-accessories/","http://www.expansys.com.sg/computing/computer-hardware+accessories/"]
    rules=[	Rule(LinkExtractor( allow = (r'.+/D+',),deny =(r'.+?filter.+',r'.+forum.+',r'.+signin.+', r'.+aspx.+','.+blog.+'))),
          	Rule(LinkExtractor( allow = (r'.+/?page.+',),deny =(r'.+?filter.+',r'.+forum.+',r'.+signin.+', r'.+aspx.+','.+blog.+'))),
            Rule(LinkExtractor( allow = (r'.+/.+\d\d\d\d\d\d/',),deny =(r'.+?filter.+',r'.+forum.+',r'.+signin.+', r'.+aspx.+','.+blog.+')), callback='parse_grid_contents',follow = True),  
           # Rule(LinkExtractor(allow=('item\.php', )))
          
          ]
    lnkk=[]
    def parse_grid_contents(self,response):
        print "got in hsadfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffere"
        for r in response.xpath('//html'):
             
            item = ExpansyscrawlItem()
            print "got in here"
            if r.xpath('//link/@href')[0].extract() not in self.lnkk and r.xpath('//h1[@itemprop="name"]/text()'):
                item['title'] = r.xpath('//h1[@itemprop="name"]/text()').extract()
                item['link'] =  r.xpath('//link/@href')[0].extract()
                
                if not r.xpath('//li[@class="instock"]')  and not  r.xpath('//li[@class="infostock"]'):
                    item['price'] = r.xpath('//p[@id="price"]/strong/text()').extract() + r.xpath('//p[@id="price"]/sup/text()')
                #    print r.xpath('//p[@id="price"]/strong/text()')[0].extract() + " no dot"
                    
                else:
                    item['price'] = r.xpath(r'//p[@id ="price"]//span/text()').extract() + r.xpath('//p[@id ="price"]//span/sup/text()').extract()
               #     print r.xpath(r'//span[@itemprop="price"]/text()')[0].extract()
                    
                item['currency'] = r.xpath('//p[@id="price"]/meta/@content').extract()
                m = re.search(r'sku:(\d+)',r.xpath('//ul[@class="product-sku"]/li/span/@content')[0].extract())
                item['sku']=m.group(0)
                n = re.search(r'ean:(\d+)',r.xpath('//ul[@class="product-sku"]/li/span/@content')[1].extract())
                if n:
                    item['ean'] = n.group(0)
                item['brand'] = r.xpath('//ul[@class="product-sku"]/li/a/text()').extract()
                item['primary_image_url']=r.xpath('//a[@class ="js-primary-image-link"]/@href').extract()
                item['time'] =self.now.strftime("%Y-%m-%d %H:%M")
                self.lnkk.append(r.xpath('//link/@href')[0].extract())
            
                item['category'] =r.xpath('//ul[@id="breadcrumbs"]//span/text()').extract()
            #item['desc']=r.xpath('//div[@class="what_we_say"]/text()').extract()
            yield item