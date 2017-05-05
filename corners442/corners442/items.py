# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Corners442Item(scrapy.Item):
    # General match info
    match_id = scrapy.Field()
    league_id = scrapy.Field()
    season = scrapy.Field()
    team_name = scrapy.Field()
    host_status = scrapy.Field()  # 0 - guest team, 1 - host team
    team_score = scrapy.Field()  # how many goals the team've scored
    scoring_minutes = scrapy.Field()  # minutes of the goals been scored

    # Corners info
    corners_total = scrapy.Field()
    corners_chances_created = scrapy.Field()
    corners_assists = scrapy.Field()
    corners_failed = scrapy.Field()


class LeagueItem(scrapy.Item):
    league_id = scrapy.Field()
    league_name = scrapy.Field()