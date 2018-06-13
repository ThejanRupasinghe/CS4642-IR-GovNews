import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"

    # Adds all page urls
    start_urls = [
        'http://powermin.gov.lk/english/?cat=14'
    ]
    for i in range(2, 41):
        start_urls.append("http://powermin.gov.lk/english/?cat=14&paged=" + str(i))

    def parse(self, response):
        # follow links to article page with "Read more" button link
        for href in response.css('div.post a.button::attr(href)'):
            yield response.follow(href, self.parse_news_page)

    def parse_news_page(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        name = extract_with_css('div.post p::text')[3]
        name = name.encode('ascii', errors='ignore')

        yield {
            'name': name
            # 'birthdate': extract_with_css('.author-born-date::text'),
            # 'bio': extract_with_css('.author-description::text'),
        }
