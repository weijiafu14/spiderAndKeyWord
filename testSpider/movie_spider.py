import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'movie'
    start_urls = [
        'http://www.dianying.com/jt/stats/yearly.php',
    ]

    def parse(self, response):
        for quote in response.css('span.type_feature'):
            href = quote.css('a::attr("href")').get()
            if href is not None:
                yield response.follow(href, self.parse_movie)

    def parse_movie(self,response):
        for tr in response.css('tr.evenrowcast'):
            href = tr.css('a::attr("href")').get()
            name = tr.css('a::text').get()
            if href is not None:
                yield {
                    'name': name
                }
        for tr in response.css('tr.oddrowcast'):
            href = tr.css('a::attr("href")').get()
            name = tr.css('a::text').get()
            if href is not None:
                yield {
                    'name': name
                }
        hrefList = response.xpath('///div[@id="page_main"]/div[@id="section_main"]/a[contains(@href, "feature")]/@href').getall()
        pagesNum = len(hrefList)/2
        for index in range(pagesNum):
            yield response.follow(hrefList[index],self.parse_movie_otherPage)

    def parse_movie_otherPage(self,response):
        for tr in response.css('tr.evenrowcast'):
            href = tr.css('a::attr("href")').get()
            name = tr.css('a::text').get()
            if href is not None:
                yield {
                    'name': name
                }
        for tr in response.css('tr.oddrowcast'):
            href = tr.css('a::attr("href")').get()
            name = tr.css('a::text').get()
            if href is not None:
                yield {
                    'name': name
                }
