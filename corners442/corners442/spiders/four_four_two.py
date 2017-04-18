from asyncio.tasks import sleep
from urllib.parse import urljoin

from scrapy.http.request import Request
from scrapy.item import Item, Field
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Spider

from ..items import Corners442Item

BASE_URL = 'https://www.fourfourtwo.com/'

class NoTeamStatsHref(Exception):
    pass


class MySpider(Spider):
    handle_httpstatus_list = [429,]
    name = 'fourfourtwo'

    def get_league_id(self):
        """Return league id by league name"""
        if self.league.lower() == 'italy':
            return 21

    def start_requests(self):

        league_id = self.get_league_id()
        url = 'https://www.fourfourtwo.com/statszone/results/{}-{}'.format(
            league_id, self.year)
        yield Request(url, self.get_links)

    def get_links(self, response):
        if response.status > 300:
            self.logger.info('HEADERS: %s', response.headers)
            import pdb
            pdb.set_trace()

        # get matches_results links:
        for link in response.xpath('//td[@class="link-to-match"]/a/@href').extract():
            yield Request(urljoin(BASE_URL, link), callback=self.get_match_info)

    def get_match_info(self, response):

        item = Corners442Item()
        item['host_team_name'] = response.xpath('//div[@class="score-wrapper"]/span[@class="home-head"]/text()').extract_first().strip()
        item['guest_team_name'] = response.xpath('//div[@class="score-wrapper"]/span[@class="away-head"]/text()').extract_first().strip()

        score = response.xpath('//div[@class="score-wrapper"]/span[@class="score"]/text()').extract_first()
        item['host_team_score'] = score.split('-')[0].strip()
        item['guest_team_score'] = score.split('-')[1].strip()

        item['host_team_goal_times'] = response.xpath('//div[@class="results"]/div[@class="home"]/span[@class="goal"]/text()|//div[@class="results"]/div[@class="home"]/span[@class="penalty"]/text()').re(r'\W*\w+\W*(\d+)\W*')
        item['guest_team_goal_times'] = response.xpath('//div[@class="results"]/div[@class="away"]/span[@class="goal"]/text()|//div[@class="results"]/div[@class="away"]/span[@class="penalty"]/text()').re(r'\W*(\d+)\W*\w+\W*')

        team_stats_link = response.xpath("//li/a[contains(., 'Team Stats')]/@href").extract_first()
        if not team_stats_link:
            raise NoTeamStatsHref

        # this will open corners info instead of overall info
        team_stats_link = team_stats_link.replace('OVERALL_01', '2_ATTACK_03')
        home_team_stats_url = urljoin(BASE_URL, team_stats_link)

        self.logger.info('Item: %s', item)
        request = Request(home_team_stats_url, callback=self.get_host_corners_info)
        request.meta['item'] = item
        yield request

    def get_host_corners_info(self, response):
        item = response.meta['item']

        corners = response.xpath('//svg[@id="pitch"]/line/@marker-end').extract()
        item['host_corners_total'] = len(corners)
        item['host_corners_chances_created'] = len([i for i in corners if i.find('#smalldarkgrey') != -1])
        item['host_corners_assists'] = len(
            [i for i in corners if i.find('#smallyellow') != -1])
        item['host_corners_failed'] = len(
            [i for i in corners if i.find('#smallred') != -1])

        self.logger.info('Item: %s', item)

        guest_team_stat_link = response.xpath('//li[@class="1 last"]/a/@href').extract_first()
        guest_team_stats_url = urljoin(BASE_URL, guest_team_stat_link)
        request = Request(guest_team_stats_url,
                          callback=self.get_guest_corners_info)
        request.meta['item'] = item
        yield request

    def get_guest_corners_info(self, response):
        item = response.meta['item']

        corners = response.xpath('//svg[@id="pitch"]/line/@marker-end').extract()
        item['guest_corners_total'] = len(corners)
        item['guest_corners_chances_created'] = len([i for i in corners if i.find('#smalldarkgrey') != -1])
        item['guest_corners_assists'] = len(
            [i for i in corners if i.find('#smallyellow') != -1])
        item['guest_corners_failed'] = len(
            [i for i in corners if i.find('#smallred') != -1])

        self.logger.info('Item: %s', item)

        yield item
