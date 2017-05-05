# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm.session import sessionmaker

from .db import League, TeamStats, get_or_create, create_session, \
    update_or_create


class Corners442Pipeline(object):

    def process_item(self, item, spider):
        # simply add or update item into database
        match_id = item.pop('match_id')
        team_name = item.pop('team_name')

        update_or_create(create_session(), TeamStats, defaults=item,
                         match_id=match_id,
                         team_name=team_name)


class LeaguePipeline(object):

    def process_item(self, item, spider):
        # simply add item to database
        get_or_create(create_session(), League, **item)
