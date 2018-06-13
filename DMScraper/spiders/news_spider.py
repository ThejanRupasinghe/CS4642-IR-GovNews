import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'http://powermin.gov.lk/english/?cat=14'
    ]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('div.post a.button::attr(href)'):
            print(href)
            yield response.follow(href, self.parse_news_page)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_news_page(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
            'name': extract_with_css('div.post p::text')
            # 'birthdate': extract_with_css('.author-born-date::text'),
            # 'bio': extract_with_css('.author-description::text'),
        }