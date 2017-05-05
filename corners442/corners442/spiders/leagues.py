from scrapy.http.request import Request
from scrapy.spiders import Spider

from ..settings import BASE_URL
from ..items import LeagueItem


class MySpider(Spider):
    name = 'league'
    custom_settings = {
        'ITEM_PIPELINES': {
            'corners442.pipelines.LeaguePipeline': 300
        }
    }

    def start_requests(self):

        yield Request(BASE_URL, self.parse)

    def parse(self, response):
        # get competitions name and id:
        for option in response.xpath('//select[@id="edit-competitions"]/option'):
            if option.xpath('@selected').extract_first(
                    default='') == 'selected':
                continue
            item = LeagueItem()
            item['league_id'] = option.xpath('@value').extract_first()
            item['league_name'] = option.xpath('text()').extract_first()
            yield item
