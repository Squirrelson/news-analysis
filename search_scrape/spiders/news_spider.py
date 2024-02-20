from pathlib import Path

import scrapy
import json

# Load JSON data from external file
with open('urls.json', 'r') as file:
    data = json.load(file)

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = data.get('allowed_domain')
    start_urls = data.get('start_url')

    def start_requests(self):
        for page_no in range(1, 500):
            # Send a POST request with the custom payload
            yield scrapy.FormRequest(
                url = self.start_urls[0],
                formdata = {
                    'page_no': str(page_no),
                    'search_txt': 'canada',
                    # Add more key-value pairs as needed
                    },
                callback = self.parse,
                meta={'page_no': page_no}
            )

    def parse(self, response):
        # Path('test.html').write_bytes(response.body)
        page_no = response.meta.get('page_no')

        for article in response.css("div.row-fluid"):
            yield {
                "headline": article.xpath('.//h4//text()').extract(),
                "link": article.css('a::attr(href)').extract(),
                "small": article.css('small::text').get(),
                "page_no": page_no
            }