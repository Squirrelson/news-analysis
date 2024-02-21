import json
import scrapy

from search_scrape.items import ArticleItem

class ArticleSpider(scrapy.Spider):
    name = 'article_spider'

    # Ingests urls from cleaned json
    def __init__(self, json_file=None, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.articles_data = self.load_articles_from_json(json_file) # List of dictionaries

    def load_articles_from_json(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data

    def start_requests(self):
        for article in self.articles_data:
            yield scrapy.Request(article['link'],
                                 callback=self.parse,
                                 meta={'url': article['link']}
                                 )

    def parse(self, response):
        url = response.meta.get('url')
        # Same as before
        item = ArticleItem()
        item['url'] = url
        item['text'] = ' '.join(response.xpath('.//div[@class="article_content"]//text()').extract()).strip()
        yield item
