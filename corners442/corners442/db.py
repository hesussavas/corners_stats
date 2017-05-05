from sqlalchemy.dialects.postgresql.array import ARRAY
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import Integer, String, Boolean

from . import settings

Base = declarative_base()


def get_engine():
    return create_engine(settings.DEV_PSQL_URI)


engine = get_engine()


def create_schema():
    Base.metadata.create_all(engine)


def create_session():
    Session = sessionmaker(bind=engine)
    return Session()


class TeamStats(Base):
    __tablename__ = 'team_stats'
    __table_args__ = (UniqueConstraint('match_id', 'team_name', name='uix_1'),)

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, index=True)
    league_id = Column(Integer, ForeignKey("league.league_id"))
    season = Column(String, index=True)
    team_name = Column(String, index=True)
    host_status = Column(Boolean)
    team_score = Column(Integer)
    scoring_minutes = Column(ARRAY(String))
    corners_total = Column(Integer)
    corners_chances_created = Column(Integer)
    corners_assists = Column(Integer)
    corners_failed = Column(Integer)


class League(Base):
    __tablename__ = 'league'

    league_id = Column(Integer, primary_key=True)
    league_name = Column(String)


def get_or_create(session, model, defaults=None, **kwargs):

    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        lookups = kwargs.copy()
        if defaults:
            for key, value in defaults.items():
                lookups[key] = value
        instance = model(**lookups)
        session.add(instance)
        session.commit()
        return instance


def update_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        lookups = kwargs.copy()
        if defaults:
            for key, value in defaults.items():
                lookups[key] = value
        for key, value in lookups.items():
            setattr(instance, key, value)
        session.commit()
        return instance
    else:
        lookups = kwargs.copy()
        if defaults:
            for key, value in defaults.items():
                lookups[key] = value
        instance = model(**lookups)
        session.add(instance)
        session.commit()
        return instance