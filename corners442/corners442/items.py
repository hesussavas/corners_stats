# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Corners442Item(scrapy.Item):
    # General match info
    host_team_name = scrapy.Field()
    guest_team_name = scrapy.Field()
    host_team_score = scrapy.Field()
    guest_team_score = scrapy.Field()
    host_team_goal_times = scrapy.Field()
    guest_team_goal_times = scrapy.Field()

    # Corners info
    host_corners_total = scrapy.Field()
    guest_corners_total = scrapy.Field()

    host_corners_chances_created = scrapy.Field()
    guest_corners_chances_created = scrapy.Field()

    host_corners_assists = scrapy.Field()
    guest_corners_assists = scrapy.Field()

    host_corners_failed = scrapy.Field()
    guest_corners_failed = scrapy.Field()

