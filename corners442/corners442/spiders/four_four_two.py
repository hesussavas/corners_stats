import re

from urllib.parse import urljoin

from scrapy.http.request import Request
from scrapy.spiders import Spider

from ..settings import BASE_URL
from ..items import Corners442Item
from ..db import create_session, League


class NoTeamStatsHref(Exception):
    pass


class MySpider(Spider):
    name = 'fourfourtwo'

    def start_requests(self):
        session = create_session()
        leagues = session.query(League).all()

        for league in leagues:
            for year in range(2010, 2015):
                url = 'https://www.fourfourtwo.com/statszone/results/{}-{}'.format(
                    league.league_id, year)
                request = Request(url, self.parse)
                request.meta['league_id'] = league.league_id
                request.meta['year'] = year
                yield request


    def parse(self, response):
        # get matches_results links:
        no_content = response.xpath(
            '//div[@id="content"]/div[@class="clear"]/text()').re(
            'There are no matches')
        if no_content:
            return

        for link in response.xpath('//td[@class="link-to-match"]/a/@href').extract():
            request = Request(urljoin(BASE_URL, link), callback=self.get_match_info)
            request.meta['match_id'] = re.search(r'^.*[/](\d+)$', link).group(1)

            request.meta['league_id'] = response.meta['league_id']
            request.meta['year'] = response.meta['year']
            yield request

    def get_match_info(self, response):

        host_team = Corners442Item(host_status=True,
                                   season=response.meta['year'],
                                   league_id=response.meta['league_id'],
                                   match_id=response.meta['match_id'])
        guest_team = Corners442Item(host_status=False,
                                    season=response.meta['year'],
                                    league_id=response.meta['league_id'],
                                    match_id=response.meta['match_id'])

        host_team['team_name'] = response.xpath('//div[@class="score-wrapper"]/span[@class="home-head"]/text()').extract_first().strip()
        guest_team['team_name'] = response.xpath('//div[@class="score-wrapper"]/span[@class="away-head"]/text()').extract_first().strip()

        score = response.xpath('//div[@class="score-wrapper"]/span[@class="score"]/text()').extract_first()
        host_team['team_score'] = int(score.split('-')[0].strip())
        guest_team['team_score'] = int(score.split('-')[1].strip())

        host_team['scoring_minutes'] = response.xpath('//div[@class="results"]/div[@class="home"]/span[@class="goal"]/text()|//div[@class="results"]/div[@class="home"]/span[@class="own_goal"]/text()|//div[@class="results"]/div[@class="home"]/span[@class="penalty"]/text()').re(r'\W*\w*\W*(\d+)\W*')
        guest_team['scoring_minutes'] = response.xpath('//div[@class="results"]/div[@class="away"]/span[@class="goal"]/text()|//div[@class="results"]/div[@class="away"]/span[@class="own_goal"]/text()|//div[@class="results"]/div[@class="away"]/span[@class="penalty"]/text()').re(r'\W*(\d+)\W*\w*\W*')

        team_stats_link = response.xpath("//li/a[contains(., 'Team Stats')]/@href").extract_first()
        if not team_stats_link:
            raise NoTeamStatsHref

        # this will open corners info instead of overall info
        team_stats_link = team_stats_link.replace('OVERALL_01', '2_ATTACK_03')
        home_team_stats_url = urljoin(BASE_URL, team_stats_link)

        request = Request(home_team_stats_url, callback=self.get_corners_info)
        request.meta['host_team'] = request.meta['team_to_fill'] = host_team
        request.meta['guest_team'] = guest_team
        yield request

    def get_corners_info(self, response):
        host_team = response.meta['host_team']
        guest_team = response.meta['guest_team']
        team_to_fill = response.meta['team_to_fill']

        corners = response.xpath(
            '//svg[@id="pitch"]/line/@marker-end').extract()
        team_to_fill['corners_total'] = len(corners)
        team_to_fill['corners_chances_created'] = len(
            [i for i in corners if i.find('#smalldarkgrey') != -1])
        team_to_fill['corners_assists'] = len(
            [i for i in corners if i.find('#smallyellow') != -1])
        team_to_fill['corners_failed'] = len(
            [i for i in corners if i.find('#smallred') != -1])

        guest_team_stat_link = response.xpath(
            '//li[@class="1 last"]/a/@href').extract_first()
        if not guest_team_stat_link:
            # in this case team_to_fill will be equals to the guest_team
            for team in [host_team, team_to_fill]:
                yield team

        else:
            guest_team_stats_url = urljoin(BASE_URL, guest_team_stat_link)
            request = Request(guest_team_stats_url, callback=self.get_corners_info)

            # if we reached here, then team_to_fill == host_team
            request.meta['host_team'] = team_to_fill
            request.meta['guest_team'] = request.meta['team_to_fill'] = guest_team
            yield request
