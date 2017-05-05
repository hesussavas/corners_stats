import random
from collections import defaultdict, OrderedDict
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from corners442.corners442.db import engine


# -- ANALYSIS CONSTANTS --

INTERESTING_TEAMS = (
    ("Manchester United", 8),
    ("Manchester City", 8),
    ("Chelsea", 8),
    ("Tottenham Hotspur", 8),
    ("Arsenal", 8),
    ("Liverpool", 8),
    ("Leicester City", 8),
    ("West Bromwich Albion", 8),
    ("Juventus", 21),
    ("Napoli", 21),
    ("Roma", 21),
    ("Internazionale", 21),
    ("Milan", 21),
    ("Barcelona", 23),
    ("Real Madrid", 23),
    ("Atlético de Madrid", 23),
    ("Sevilla", 23),
    ("Villarreal", 23),
    ("Athletic Club", 23),
    ("Celta de Vigo", 23),
    ("Valencia", 23),
    ("FC Bayern München", 22),
    ("Borussia Dortmund", 22),
    ("Bayer 04 Leverkusen", 22),
    ("VfL Wolfsburg", 22),
    ("Borussia Mönchengladbach", 22),
    ("Paris Saint-Germain", 24),
    ("Lyon", 24),
    ("Monaco", 24),
)

TOP5_LEAGUES = {22: "German Bundesliga",
                23: "Spain La Liga",
                24: "France League 1",
                8: "England Premier League",
                21: "Italy Serie A"}

LEAGUES_EXTENDED = dict(TOP5_LEAGUES, **{"98": "MLS"})


SEASONS = range(2010, 2017)

# boolean parameter means sort in ascending order or not
FEATURES = (
    ('matches_to_score_from_corner', True),
    ('percent_of_goals_scored_from_corners', False),
    ('percent_of_corners_leads_to_goal', False),
    ('percent_of_corners_chances_created_became_a_goal', False),
    ('percent_of_corners_leads_to_nothing', True),
    ('average_corners_per_match', False),
)

team_stats = pd.read_sql_query('select * from team_stats;', con=engine)


def _aggregate(data_set):
    """
    Aggregates inputted data, by creating some tricky metrics
    """
    agg = data_set.agg({"corners_assists": ["sum", "mean"],
                        "corners_failed": ["sum", "mean"],
                        "corners_chances_created": ["sum", "mean"],
                        "corners_total": ["sum", "mean"],
                        "match_id": "count",
                        "team_score": "sum",
                        })
    # add more metrics
    agg['matches_to_score_from_corner'] = 1 / agg['corners_assists']['mean']
    agg['percent_of_goals_scored_from_corners'] = (agg['corners_assists']['sum'] /
                                                   agg['team_score']['sum'] * 100)
    agg['percent_of_corners_leads_to_goal'] = (agg['corners_assists']['sum'] /
                                               agg['corners_total']['sum'] * 100)
    agg['percent_of_corners_leads_to_nothing'] = (agg['corners_failed']['sum'] /
                                                  agg['corners_total']['sum'] * 100)
    agg['percent_of_corners_chances_created_became_a_goal'] = (agg['corners_assists']['sum'] /
                                                               agg['corners_chances_created']['sum'] * 100)
    agg['matches_played'] = agg['match_id']['count']
    agg['average_corners_per_match'] = agg['corners_total']['mean']

    agg = agg.reset_index()

    # make name more understandable
    agg = agg.rename(columns={'team_score': "goals_scored"})

    return agg


def get_info(team_stats, league=None, season=None, team_name=None,
             group_by=None, sort_by=None, asc=True, how_much=25,
             per_team_stat=False):
    """
    Gets the dataframe and processed it according to the set of arguments,
    which corresponds to aggregation, filtering, sorting ad limitation

    :param team_stats: basic data frame with all the collected data
    :param league: an array (!) of leagues to filter input data with them
    :param season: filter for a particular season
    :param team_name: to restrict the result for only 1 concrete team
    :param group_by: an array of columns for grouping data
    :param sort_by: an array of columns for sorting data
    :param asc: Direction of the sorting (only for the 1st column)
    :param how_much: limiting the output results amount
    :param per_team_stat: flag which means we need to sort the result by season
    :return: edited data frame with grouped, agreggated, sorted and limited data
    """

    # league filter
    if league:
        team_stats = team_stats[team_stats['league_id'].isin(league)]

    # season filter
    if season:
        team_stats = team_stats[team_stats['season'] == str(season)]

    # team_name filter
    if team_name:
        team_stats = team_stats[team_stats['team_name'] == team_name]

    # grouping
    grouped = team_stats.groupby(group_by)

    # aggregate
    aggregated = _aggregate(grouped)

    resulted_columns = ['matches_played',
                        'goals_scored',
                        'average_corners_per_match',
                        'corners_assists',
                        'matches_to_score_from_corner',
                        'percent_of_goals_scored_from_corners',
                        'percent_of_corners_leads_to_goal',
                        'percent_of_corners_chances_created_became_a_goal',
                        'percent_of_corners_leads_to_nothing']

    # append grouped columns
    for g in group_by:
        resulted_columns.append(g)

    if per_team_stat:
        sort_by = 'season'

    # sorting
    aggregated = aggregated.sort_values(sort_by, ascending=asc)
    # cleaning
    aggregated = aggregated.replace([np.inf, -np.inf], 0)

    return aggregated[resulted_columns][:how_much]


def get_scoring_minutes():
    """
    Creates a dict with a structure like: {"minute": goals_scored}, so we
    could understand what minute is the most popular to score on.
    """

    # use matches without extra times
    leagues = (8, 21, 22, 23, 24, 98, 214)
    _team_stats = team_stats[team_stats['league_id'].isin(leagues)]
    minutes = _team_stats['scoring_minutes'].values

    result = defaultdict(int)

    for mins in minutes:
        for m in mins:
            try:
                result[int(m)] += 1
            except ValueError:
                pass

    return OrderedDict(((k, result[k]) for k in sorted(result.keys())))


def create_minutes_plot(data):
    """
    Draws the plot for scoring minutes
    """

    fig, ax = plt.subplots(figsize=(15, 8))

    barlist = ax.bar(list(data.keys()), data.values())
    for i, b in enumerate(barlist, start=1):
        if i % 2 == 0:
            b.set_color('0.75')
        else:
            b.set_color('0.55')

    ax.set_xticks(np.arange(len(data)))
    ax.set_yticks(np.arange(0, max(data.values()), 25))
    ax.set_xticklabels(list(data.keys()), rotation='vertical')

    # 100 minutes is enough
    for i, y in enumerate(list(data.values())[:100]):
        plt.text(i - 0.5, y, y, fontweight='bold', fontsize=5)

    ax.set_ylim((0, 450))
    ax.set_xlim((0, 100))
    plt.xlabel('Match minutes')
    plt.title('Goals scored per minute.\n'
              'Scored in the first half:{}\n'
              'Scored in the second half:{}'.format(
        sum((value for key, value in data.items() if key <= 45)),
        sum((value for key, value in data.items() if key > 45))))
    plt.ylabel('Number of goals')
    plt.savefig(_get_path('goals_minutes', 'goals_minutes'), dpi=200)


def create_bar_plots(info, title, filename, x_label, y_label):
    """
    Draws bar plots and save them as files
    :param info: processed data frame with aggregated and sorted data
    :param title: title for a plot
    :param filename: filename to save concrete plot with
    :param x_label: what's on the x-axis
    :param y_label: what's on the y-axis
    :return: None
    """

    fig, ax = plt.subplots(figsize=(15, 9))
    ind = np.arange(len(info))
    ax.bar(ind, info[y_label], color=random.choice('rgbycm'))
    ax.set_xlabel(x_label)
    ax.set_ylabel(" ".join(y_label.split("_")))

    for tick in ax.yaxis.get_major_ticks():
        tick.label1On = False
        tick.label2On = True
        tick.label2.set_color('green')

    ax.set_xticks(np.arange(len(info)))

    ax.set_xticklabels(info[x_label].values,
                       rotation='vertical')

    plt.subplots_adjust(bottom=0.3)
    for i, y in enumerate(info[y_label]):
        plt.text(i - 0.3, y, "{:.2f}".format(y), fontweight='bold', fontsize=7)

    plt.title(title)
    plt.savefig(_get_path(y_label, filename), dpi=200)
    plt.close('all')


def _get_path(subdir, filename):
    """
    Creates a path for an image
    :param subdir: directory to store images in
    :param filename: name of the outputted file
    :return: string representation of the path
    """
    path = Path('files', 'images', subdir)
    path.mkdir(exist_ok=True, parents=True)

    return str(path / filename)


def build_per_league_stat():
    for league_id, league_name in LEAGUES_EXTENDED.items():
        for season in SEASONS:
            for feature, asc in FEATURES:
                data = get_info(team_stats, league=[league_id], season=season,
                                group_by=['team_name', 'season'],
                                sort_by=feature, asc=asc)
                title = "{} \n {}".format(league_name,
                                          "{}/{}".format(season, season + 1))
                filename = "{}.png".format(league_name + "_" + str(season))
                create_bar_plots(data, title, filename, x_label='team_name',
                                 y_label=feature)


def build_leagues_average_by_season():
    for feature, asc in FEATURES:
        for season in SEASONS:
            data = get_info(team_stats, league=LEAGUES_EXTENDED.keys(),
                            season=season,
                            group_by=['league_id', 'season'],
                            sort_by=[feature], asc=asc)
            title = "Leagues average for {}/{} season. \n" \
                    "Mappings: {}".format(season, season + 1, LEAGUES_EXTENDED)
            filename = "Average_by_league_{}.png".format(season)
            create_bar_plots(data, title, filename, x_label='league_id',
                             y_label=feature)


def build_per_team_stat():
    for team, league in INTERESTING_TEAMS:
        for feature, asc in FEATURES:
            # Here we use always asc = True, cause we will iterate through
            # years (seasons) and they'd better be in ascending order :)
            data = get_info(team_stats, league=[league],
                            group_by=['team_name', 'season'],
                            team_name=team,
                            sort_by=feature, asc=True, how_much=7,
                            per_team_stat=True)
            title = "{} \n {}".format(team, TOP5_LEAGUES[league])
            filename = "{}_{}.png".format(team, TOP5_LEAGUES[league])
            create_bar_plots(data, title, filename, x_label='season',
                             y_label=feature)


def build_general_results_for_top20_for_all_time():
    for feature, asc in FEATURES:
        data = get_info(team_stats, league=TOP5_LEAGUES.keys(),
                        group_by=['team_name', 'season'],
                        sort_by=feature, asc=asc)
        title = "TOP-20 results through seasons"
        filename = "top20_{}.png".format(feature)
        create_bar_plots(data, title, filename,
                         x_label=['team_name', 'season'],
                         y_label=feature)


def build_general_results_for_top20_by_season():
    for feature, asc in FEATURES:
        for season in SEASONS:
            data = get_info(team_stats, league=TOP5_LEAGUES.keys(),
                            season=season,
                            group_by=['team_name', 'season'],
                            sort_by=feature, asc=asc)
            title = "TOP-20 results through for season {}/{}".format(season,
                                                                     season + 1)
            filename = "top20_{}_{}.png".format(feature, season)
            create_bar_plots(data, title, filename,
                             x_label='team_name',
                             y_label=feature)


def build_per_team_stat_cl():
    league_id, league_name = 5, 'Champions League'
    for team, _ in INTERESTING_TEAMS:
        for feature, asc in FEATURES:
            # asc = True, cause we will iterate through years (seasons)
            data = get_info(team_stats, league=[league_id],
                            group_by=['team_name', 'season'], team_name=team,
                            sort_by=feature, asc=True, how_much=7,
                            per_team_stat=True)
            title = "{} \n {}".format(team, league_name)
            filename = "{}_{}.png".format(team, league_name)
            create_bar_plots(data, title, filename, x_label='season',
                             y_label=feature)


if __name__ == "__main__":
    create_minutes_plot(get_scoring_minutes())
    build_per_team_stat_cl()
    build_per_team_stat()
    build_per_league_stat()
    build_leagues_average_by_season()
    build_general_results_for_top20_by_season()
    build_general_results_for_top20_for_all_time()
