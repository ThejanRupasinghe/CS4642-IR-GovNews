import scrapy
import json


class EnergyNewsSpider(scrapy.Spider):
    name = "energy_news"

    # Adds all page urls
    start_urls = [
        'http://powermin.gov.lk/english/?cat=14'
    ]

    for i in range(2, 46):
        start_urls.append("http://powermin.gov.lk/english/?cat=14&paged=" + str(i))

    def parse(self, response):
        # follow links to article page with "Read more" button link
        for href in response.css('div.post a.button::attr(href)'):
            yield response.follow(href, self.parse_news_page)

    def parse_news_page(self, response):

        # scrapping date
        date_month = response.xpath('//div[@class="inner-t"]/a/span[@class="post-date"]/text()').extract_first()
        date_arr = response.xpath('//div[@class="inner-t"]/a/span')
        date = ""
        for raw in date_arr:
            if not raw.xpath("@class").extract():
                date += raw.xpath('text()').extract_first().encode('ascii', errors='ignore')
        date += " " + date_month

        # scrapping title of the article
        title = response.xpath('//div[@class="heading bott-15"]/h3/a/text()').extract_first().encode('ascii',
                                                                                                     errors='ignore')
        # article text
        text_arr = response.xpath('//div[@class="post"]/p')
        text = ""
        for para in text_arr:
            if (para.xpath("@class").extract() == []) and para.xpath("@align").extract() == []:
                raw_text = para.xpath('text()').extract_first()
                if raw_text is not None:
                    text += raw_text.encode('ascii', errors='ignore')
                    text += "\n"

        if not (text == "" or text == "\n\n"):
            output = {
                'date': date,
                'title': title,
                'text': text,
                'url': response.url
            }

            # data_file = open("energy_news_data.json", "a+")
            # data_file.write(json.dumps(output, indent=2, sort_keys=True))
            # data_file.write(",\n")
            # data_file.close()

            url = response.url
            file_name = url[-4:]

            data_file = open("data_energy_news/" + file_name + ".json", "w+")
            data_file.write(json.dumps(output, indent=2, sort_keys=True))
            data_file.close()

            yield {
                'date': date,
                'title': title,
                'text': text,
                'url': response.url
            }
