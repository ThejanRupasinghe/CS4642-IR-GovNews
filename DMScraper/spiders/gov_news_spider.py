import scrapy
import json


class GovNewsSpider(scrapy.Spider):
    name = "gov_news"

    # Adds all page urls
    start_urls = [
        'https://www.dgi.gov.lk/news/latest-news?limitstart=0'
    ]

    for i in range(1, 128):
        start_urls.append("https://www.dgi.gov.lk/news/latest-news?start=" + str(i * 10))

    def parse(self, response):
        # follow links to article page with "Read more" button link
        for href in response.css('p.readmore a::attr(href)'):
            yield response.follow(href, self.parse_news_page)

    def parse_news_page(self, response):

        date = response.xpath('//dd[@class="published"]/time/text()').extract_first().replace("\t", "").replace("\n",
                                                                                                                "")
        title = response.xpath('//h2[@itemprop="name"]/text()').extract_first().replace("\t", "").replace("\n",
                                                                                                          "").encode(
            'ascii', errors='ignore')

        text_paras = response.xpath('//div[@itemprop="articleBody"]/div[@class="itemFullText"]/p')
        text_paras += response.xpath('//div[@itemprop="articleBody"]/p')
        text_paras += response.xpath('//div[@itemprop="articleBody"]/div[@class="itemFullText"]/p/em')
        text_paras += response.xpath('//div[@itemprop="articleBody"]/div[@style="text-align: justify;"]')
        text_paras += response.xpath('//div[@itemprop="articleBody"]/div')
        text = ""
        for para in text_paras:
            raw_text = para.xpath('normalize-space()').extract_first()
            # raw_text = raw_text.xpath('text()').extract_first()
            if raw_text is not None:
                text_before = raw_text.encode('ascii', errors='ignore')
                if not (text_before == "Twitter"):
                    text += text_before

        if not (text == ""):
            output = {
                'date': date,
                'title': title,
                'text': text,
                'url': response.url
            }

            url = response.url
            file_name = url[40:44]

            data_file = open("data_gov_news/" + file_name + ".json", "w+")
            data_file.write(json.dumps(output, indent=2, sort_keys=True))
            data_file.close()

            yield {
                'date': date,
                'title': title,
                'text': text,
                'url': response.url
            }
