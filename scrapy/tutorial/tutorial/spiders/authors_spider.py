import scrapy 

class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        ## 作者頁面
        for href in response.css(".author+a::attr(href)").extract():
            author_url = response.urljoin(href)
            yield scrapy.Request(author_url, callback = self.parse_author)
        ## 翻頁
        for href in response.css(".next a::attr(href)").extract_first():
            page_url = response.urljoin(href)
            yield scrapy.Request(page_url, callback = self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
        