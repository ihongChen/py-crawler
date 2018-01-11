import scrapy 
import logging
from datetime import datetime

class PTTSpider(scrapy.Spider):
    name = 'ptt' # 此名稱唯一且從cmd呼叫
    allowed_domain = ['ptt']
    start_urls = [
        # 'https://www.ptt.cc/bbs/Gossiping/index.html',
        'https://www.ptt.cc/bbs/movie/index.html',
    ]

    _retries = 0
    _pages = 0 

    MAX_RETRY = 1

    COOKIES = {'over18':1}
    MAX_PAGES = 2
    

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse, cookies=PTTSpider.COOKIES)

    def parse(self, response):
        """看板頁面取得內文連結"""
        
        # 想檢查其中的response
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        # print(response.text)
        self._pages += 1
        
        for post in response.css('.r-ent'):
            post_url = response.urljoin(post.css('.title a::attr(href)').extract_first())
            yield scrapy.Request(post_url, callback=self.parse_post, cookies=PTTSpider.COOKIES)
            # yield {
            #     'title' : post.css('.title a::text').extract_first(),
            #     'url' : response.urljoin(post.css('.title a::attr(href)').extract_first()),                    
            # }
        if self._pages < PTTSpider.MAX_PAGES:
            
            next_page = response.css('.btn.wide')
            if next_page:
                url = response.urljoin(next_page[1].css('::attr(href)').extract_first())
                logging.warning('follow {}'.format(url))
                yield scrapy.Request(url, callback=self.parse)
            else:
                logging.warning('no next page')
        else:
            logging.warning('max pages reached!!')


    def parse_post(self, response):
        """每篇內文文章 """
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = {}

        try:
            author, board, title, post_time_str = response.css('.article-meta-value::text').extract()
        except ValueError :
            raise ValueError('無作者/標題/發文時間...訊息')

        content = ''.join(response.css('#main-content::text').extract())        
        ### 推噓文 ####
        comments = []
        total_score = 0
        for comment in response.css('.push'):
            push_tag = comment.css('.push-tag::text').extract_first()
            push_user = comment.css('.push-userid::text').extract_first()
            push_content = comment.css('.push-content::text').extract_first()

            if '推' in push_tag:
                score =1
            elif '噓' in push_tag:
                score = -1
            else:
                score = 0

            total_score += score

            comments.append({
                'user': push_user,
                'content': push_content,
                'score' : score
            })

        item['title'] = title
        item['board'] = board
        item['author'] = author
        item['post_time'] = datetime.strptime(post_time_str,'%a %b %d %H:%M:%S %Y')
        item['comments'] = comments
        item['score'] = total_score
        item['url'] = response.url
        yield item
