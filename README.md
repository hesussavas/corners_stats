# Statistical project on soccer's corners.


Tech details
============

First part of the project - data scraping.
Second part - analysis itself and graphics.

In order to run the first part - run this command:
```make start_scraping```

Script will do the following:
- creates docker-container with the postgres DB, 
- creates DB schema, 
- scrapes leagues names and ids 
- scrapes corners stats.
- save everything into the DB.

When the scraping is over and your database is full of data, then you can run 
analysis script, which analyses data and builds plots. 
Use the following command:
``` make analysis ```

The analysis script takes some time to run (about 5 minutes, depending on your 
hardware). It won't print any messages. Just be patient.
It will create a bunch of images with plots under the 
[/files/images/](/files/images/) folder.

Preface
=======
This project was inspired by an interesting book by Chris Anderson & David Sally
[The Numbers Game: Why Everything You Know About Soccer Is Wrong](https://www.goodreads.com/book/show/17465493-the-numbers-game)

In the chapter __Reforming Beliefs with Data and Analysis__
they've tried to proof a simple statement:
  > “corners lead to shots, shots lead to goals. Corners, then, should lead to goals”

They've examined 134 EPL matches from the 2010/11 season with a total of 1434 
corners. And they got some shocking results:
- only 20% of corners lead to a shot on goal.
- only 10% of this shots lead to goal.  
In other words: **Only 2% of corners leads to goal**

That was impressive. So impressive, that I decided to google for other artiles
about the influence of the corners. I've 
[found](http://talksport.com/football/surprising-stats-pl-teams-most-likely-score-corners-150127133651) 
a [couple](http://www.scienceofsocceronline.com/2010/12/corner-kicks-by-numbers.html),
but wasn't satisfied by them: most of them were about EPL and considered the data for 1 season maximum.

So, I decided to do something similar by my own. But with a bunch of data.


FAQ
===
**Question:** What is the target of scraping?  
**Answer:** Scraping is running for https://www.fourfourtwo.com/statszone/  

**Question:** What kind of data is scraped?  
**Answer:** For each match the following information is scraped:
- total corners amount
- amount of corners leading to nothing (team loses the ball)
- amount of corners leading to chance creation
- amount of corners leading to assist
- match total score
- scoring minutes for each goal

All this information is represented by arrows on the field, where the arrow's
color determine the type of event. [Example](https://www.fourfourtwo.com/statszone/5-2013/matches/750261/team-stats/186/2_ATTACK_03#tabs-wrapper-anchor)

**Question:** What is considered as a "goal from corner"?  
**Answer:** In this project only "the second touch goals" is analysed.  
That mean the simplest scheme: Cross from corner -> Shot. No 3rd touch. 
No intermediate passes. No direct goals from the corner spot.
Why? Cause statszone represents data only in that manner.
  
**Question:** What leagues and seasons are presented in the scraped data?  
**Answer**: This script scrapes all the leagues and seasons presented in the 
statszone. Here they are:  

| **League**          | **Seasons**       |
|---------------------|-------------------|
| EPL                 | 2010\11 - 2016\17 |
| Bundesliga          | 2012\13 - 2016\17 |
| Serie A             | 2012\13 - 2016\17 |
| La Liga             | 2012\13 - 2016\17 |
| League 1            | 2012\13 - 2015\16 |
| MLS                 | 2016\17           |
| Champions League    | 2010\11 - 2016\17 |
| Europa League       | 2010\11           |
| Australian A-League | 2012\13 - 2013\14 |
| World Cup           | 2014              |
| Euro                | 2012, 2016        |  


Curious statistics
==================
**11234** matches analysed   
**115199** corners played  
**30812** goals scored  
**1459** goals came from corners  
**57,3%** of corners lead to nothing (team loses the ball)  
**26.0%** of corners are not crosses (short pass)  
**15,4%** of corners lead to chance creation  
**8.25%** chances created from corners lead to goal  
**4,74%** goals scored from corners  
**1,27%** of corners leads to goal  

**15.4** matches to wait for a goal from corner *(for a single team to score)*  
**5.13** corners per match played *(for a single team)*


Analysis
========
I've found a lot of fun things during this analysis and I'd like to share them
with the world.  
**Let's look at the teams and results we've already known through
 the prism of corners.**
  
  
There are more than 600 graphs in this project, but this text won't cover 
all of them - only the interesting ones (about 40 of them).

I've developed the following set of features to analyse for:
 * **average_corners_per_match** - average amount of corners per match
 * **matches_to_score_from_corner** - how many matches to wait, till the team scores from corner
 * **percent_of_corners_leading_to_goal** - % of corners leading to goal 
 * **percent_of_corners_leading_to_nothing** - % of corners leading to nothing
 * **percent_of_goals_scored_from_corners** - % of goals scored from corners
 
All the images for a particular feature are stored in the folder with the 
corresponding name. 

In this text I'll explore each of this features in a row. Let's start.

*(There is, also, one extra feature **percent_of_corners_chances_created_became_a_goal**, 
(% of chances, created from corners, that became a goal) which I won't cover in 
this analysis section. Don't hesitate to explore it by yourself, if you are interested.)*

### Average corners per match

Roughly it's **5.1** corner per match for a single team.
For example, top-5 leagues average for a last 2 seasons 
![Average by league 2015](https://github.com/hesussavas/corners_stats/blob/master/files/images/average_corners_per_match/Average_by_league_2015.png)
![Average by league 2016](https://github.com/hesussavas/corners_stats/blob/master/files/images/average_corners_per_match/Average_by_league_2016.png)

Let's look at the last season's results for each league. 
I see a clear trend here:_"higher the team in the table - more corners it gets"_.
Of course, there are some exceptions, but in general you can count on this trend.
![EPL](https://github.com/hesussavas/corners_stats/blob/master/files/images/average_corners_per_match/England%20Premier%20League_2016.png)
![Bundeliga](https://github.com/hesussavas/corners_stats/blob/master/files/images/average_corners_per_match/German%20Bundesliga_2016.png)
![La Liga](https://github.com/hesussavas/corners_stats/blob/master/files/images/average_corners_per_match/Spain%20La%20Liga_2016.png)
![Serie A](https://github.com/hesussavas/corners_stats/blob/master/files/images/average_corners_per_match/Italy%20Serie%20A_2016.png)
![League 1](https://github.com/hesussavas/corners_stats/blob/master/files/images/average_corners_per_match/France%20League%201_2015.png)

Does this helps them? I don't think so. You'll see it clearly a bit later, when we 
will be looking at [percent_of_corners_leading_to_goal](https://github.com/hesussavas/corners_stats#percent-of-corners-leads-to-goal) feature.

I consider corners not as an advantage, but as a missed opportunity. 
As a result of a failed attack and a success of the defence. 
So, huge amount of corners only indicates that you create a lot of chances. 
And primarily all teams from the top of the tables do so.

### Matches needed to score from corner
Those are really harsh numbers: you should wait for about **16** matches on average 
to see a goal from corner by your team.  

Again, let's look at top-5 league results for a last 2 seasons:
![Average by league 2015](https://github.com/hesussavas/corners_stats/blob/master/files/images/matches_to_score_from_corner/Average_by_league_2015.png)
![Average by league 2016](https://github.com/hesussavas/corners_stats/blob/master/files/images/matches_to_score_from_corner/Average_by_league_2016.png)
  
But for some teams it's a bit more interesting. For example, the best 
**Liverpool**'s season with **Rogers** is a bright spot. They scored from corners 
once in 4 matches, while usually they scored (and still do) only once in 
13-19 matches!
![Best season with Rogers](https://github.com/hesussavas/corners_stats/blob/master/files/images/matches_to_score_from_corner/Liverpool_England%20Premier%20League.png)

**Real Madrid** usually have a good looking numbers (3 to 7 matches), except 
for the season 2013/14 (19 matches). That was Carlo Anchelotti's first season.
Was it Mourinho's legacy? Did he ruined everything before handed the team to 
Anchelotti? I don't think so. Madrid were really great that season: they won 
the Champions League and were the top scoring team in La Liga. They just didn't
score from corners.
![Carlo's first season at RM](https://github.com/hesussavas/corners_stats/blob/master/files/images/matches_to_score_from_corner/Real%20Madrid_Spain%20La%20Liga.png)
  
Guess, when the **Atleti**-guys won La Liga?
![Atleti](https://github.com/hesussavas/corners_stats/blob/master/files/images/matches_to_score_from_corner/Atl%C3%A9tico%20de%20Madrid_Spain%20La%20Liga.png)

When **BVB** have struggled in goalscoring so badly, that they were forced to 
score at least the simplest ones. Luckily, they escaped relegation and took the 
7th place.
![BVB](https://github.com/hesussavas/corners_stats/blob/master/files/images/matches_to_score_from_corner/Borussia%20Dortmund_German%20Bundesliga.png)

And now - my favourites - **West Bromvich**.
Take a look at those graph:
![West Bromvich](https://github.com/hesussavas/corners_stats/blob/master/files/images/matches_to_score_from_corner/West%20Bromwich%20Albion_England%20Premier%20League.png)

It was an average team, scoring from corners for 2-3 times per season, while 
suddenly **Tony Pulis** took over in the middle of the 2014/15 season. 
West Brom immediately started scoring from corners way, way more frequently, 
but this fact didn't improve their league standing. Moreover, it even worsen it!  
(see https://en.wikipedia.org/wiki/List_of_West_Bromwich_Albion_F.C._seasons)

### Percent of corners leads to goal
**1,27** percents of corners is only finished with a goal! Mama mia!

Again, let check it with a leagues' average graphs
![2015](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/Average_by_league_2015.png)
![2016](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/Average_by_league_2016.png)

And now let's check each league results separately
![EPL](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/England%20Premier%20League_2016.png)
![Bundeliga](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/German%20Bundesliga_2016.png)
![La Liga](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/Spain%20La%20Liga_2016.png)
![Serie A](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/Italy%20Serie%20A_2016.png)
![League 1](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/France%20League%201_2015.png)

Do you see it? Those graphs doesn't correlate with the 
[average corners per match](https://github.com/hesussavas/corners_stats#average-corners-per-match) graphs. 
So, having a lot of corners doesn't mean you will score from them a lot. 

Let's look at some interesting teams.  
For all of 5 seasons listed in the graph **Bayern München** has less than 1% 
corners ended with a goal. So, don't hesitate to go smoking or peeing while they 
are having corner.
![Bayern München](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/FC%20Bayern%20München_German%20Bundesliga.png)
 
**Paris Saint-Germain** has an enormous percentage of successful 
corners - **13%** - in the Champions League season 2013/14. 
Probably, the best result ever for that feature.  
![PSG](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/Paris%20Saint-Germain_Champions%20League.png)

Ironically, that this enormous percentage of corners leading to goals, was 
achieved with the highest percentage (68%) of corners leading to nothing, for a 5 
years!
![PSG](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Paris%20Saint-Germain_Champions%20League.png)

But absolute champion on a long-term distance is again - my favourite - 
**West Bromvich**. They are the only team to have 2 seasons with brain-wrecking
 results of 5.2% and 6.3%. Of course, Toni Pulis was the coach for both seasons.
![West Brom](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_goal/West%20Bromwich%20Albion_England%20Premier%20League.png)

### Percent of corners leads to nothing

Unfortunately for fans, it's **57.3%**. So, the majority of the corners are wasted.  
  
Let's look at the leagues average.
You could see a clear trend here: **French League 1** has the worst numbers 
through the seasons, while **Serie A** has the best numbers. But all of them are above 50% :)
![Average by league 2012](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Average_by_league_2012.png)
![Average by league 2013](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Average_by_league_2013.png)
![Average by league 2014](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Average_by_league_2014.png)
![Average by league 2015](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Average_by_league_2015.png)
In absence of the data for French League 1 for 2016\17 season it's place was taken by MLS :)
![Average by league 2016](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Average_by_league_2016.png)

**Juve** with **Conte** and with **Allegri** (took over since 2014\15) are 2 different teams.
Especially in Champion League. Only 23% of wasted corners in 2013\14!
![Juve](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Juventus_Champions%20League.png)

**Chelsea** with **Conte** also has different result. 
The value decreased by 20% comparing with the previous season! And it 
became < 50% for the first time in 7 years!
![Chelsea](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Chelsea_England%20Premier%20League.png)

But it wasn't the best value for the last season in EPL. 
Look who's first - **Bournemouth**.
![EPL](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/England%20Premier%20League_2016.png)

You think this is a great result? Take a look at last season in **Seria A**. 
Almost half of the table has value < 50%. That's impressive.
![Italy](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Italy%20Serie%20A_2016.png)

And in contrast - **French League 1** a couple of seasons ago. 
What? **75%** of wasted corners for **Nice**? Have they ever trained corners?
![France](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/France%20League%201_2014.png)

I was confident, that in Spain - there must be only 1 possible leader for 
this feature - **Barcelona**. They don't like crosses much, so they should have
the best value for this. But look closer. The leader is **Las Palmas** with that 
breathtaking number. Who the hell they are?
![Spain](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_corners_leads_to_nothing/Spain%20La%20Liga_2016.png)


### Percent of goals scored from corners
On average - **4.74%**  
Last season's results:
![Average by league 2016](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_goals_scored_from_corners/Average_by_league_2016.png)

**Barcelona** has one of the lowest values for this feature. 
![Barca](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_goals_scored_from_corners/Barcelona_Spain%20La%20Liga.png)
**Louis Enrique** (took over in 2014\15) have increased this value to 3.6% 
percents in his first season and then constantly decreased it till they 
reached all-time minimum of **0.86%**
![all time minimum](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_goals_scored_from_corners_asc/top20_percent_of_goals_scored_from_corners.png)
Do you see it? First 3 places are occupied by Barca. That club is really hate scoring 
from corners in it's classic representation.

But now let's look at the opposite of that graph - top-20 with the highest 
percentage of goals, scored from corners.
![all time maximum](https://github.com/hesussavas/corners_stats/blob/master/files/images/percent_of_goals_scored_from_corners/top20_percent_of_goals_scored_from_corners.png)

**West Bromwich**. Again **West Bromwich**. They've scored almost quarter of 
their total goals from corners for 2 seasons! And 1/7th of the goals in 2015/16.
It turns out, that for some teams corners matters. And matters a lot.

I don't want to be impolite or insulting, but, Gosh, how boring is that! Your 
favourite team scoring decent amount of goals in such a primitive manner. 
I couldn't stand that. For sure. I can't even imagine something worse then that!  

OK. I can. A team, scoring only from penalties. 
That would be the worst team ever, I think.

But let's look at this graph from the different angle and forget for a minute about West Brom.
**8(!)** teams presented on the graph got into relegation zone in corresponding years! 
Examples:  

| Team            | Season    | Goals from corners | Comment                                                                                                                                                  |
|-----------------|-----------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Nancy           | [2012/2013](https://en.wikipedia.org/wiki/2012%E2%80%9313_Ligue_1) |         21%        |                                                                                                                                                          |
| Verona          | [2015/2016](https://en.wikipedia.org/wiki/2015%E2%80%9316_Serie_A) |        20.6%       |                                                                                                                                                          |
| Cardiff City    | [2013/2014](https://en.wikipedia.org/wiki/2013%E2%80%9314_Premier_League) |       18.75%       |                                                                                                                                                          |
| Fulham          | [2013/2014](https://en.wikipedia.org/wiki/2013%E2%80%9314_Premier_League) |         15%        |                                                                                                                                                          |
| Middlesborough  | [2016/2017](https://en.wikipedia.org/wiki/2016%E2%80%9317_Premier_League) |        14.8%       |                                                                                                                                                          |
| Wolfsburg       | [2016/2017](https://en.wikipedia.org/wiki/2016%E2%80%9317_Bundesliga) |        14.7%       | they win their relegation play-offs and stayed at Bundesliga                                                                                         |
| Eibar           | [2014/2015](https://en.wikipedia.org/wiki/2014%E2%80%9315_La_Liga) |        14.7%       | they took 18th place and should have been relegated, but escaped it due to Elche's [financial problems](http://www.laliga.es/en/news/official-statement-27) |
| Real Valladolid | [2013/2014](https://en.wikipedia.org/wiki/2013%E2%80%9314_La_Liga) |       13.16%       |                                                                                                                                                          |

**8 teams!** And **5** more escaped relegation zone miraculously (probably, thanks to goals from corners :)  

| Team            | Season    | Goals from corners | League position   | Comment                          |
|-----------------|-----------|--------------------|-------------------|----------------------------------|
| Sochaux         | [2012/2013](https://en.wikipedia.org/wiki/2012%E2%80%9313_Ligue_1) |         14.6%      |  15th out of 20   | 3 points from relegation zone    |
| FSV Mainz 05    | [2016/2017](https://en.wikipedia.org/wiki/2016%E2%80%9317_Bundesliga) |         13.6%      |  15th out of 18   | points parity with 16th Wolfsburg|
| Genoa           | [2012/2013](https://en.wikipedia.org/wiki/2011%E2%80%9312_Serie_A) |        13.16%      |  17th out of 20   | 6 points from relegation zone    |
| Osasuna         | [2012/2013](https://en.wikipedia.org/wiki/2012%E2%80%9313_La_Liga) |        12.12%      |  16th out of 20   | 3 points from relegation zone    |
| Guingamp        | [2013/2014](https://en.wikipedia.org/wiki/2013%E2%80%9314_Ligue_1) |       11.76%       |  16th out of 20   | 2 points from relegation zone    |


### Conclusion
So, I'm about to make an extraordinary conclusion out of this:
> The more team scores from corners, the greater chances for this team to be relegated

Paradox? Sure, but, I think, I have an explanation for it.

Modern football is a complicated, tactical game. It's more productive to play 
short on corner and then try to create positional attack. Or play the corner
in a non-standard way, so that the opponent won't be able to cope with it. 

Football is developing rapidly - you can't ignore it and just trust in corner 
crosses. And if you do so, then it indicates that your team is tactically weak 
and uncreative in offence. And you're doomed to lose against fit, tactically 
trained teams and sometimes you could even get relegated.

You could ask me: "But why West Bromwich's never got relegated according to your 
logic? They have join "the risk group" for a 3 times!"

But football is not only about scoring goals. It also about defending. And it's
hard to tell which part of the game is more important. Perhaps, the best option - 
is a balance of defence and offence. Cause not conceding a goal will guarantee 
you at least 1 point. And scoring 1 primitive goal from corner could give you 3 points.
And it seems to me, West Brom are good at it: *to stay in defence and then 
to score from a random corner.*
Therefore, all those relegated and semi-relegated teams not only lacked
creativity in attack, but, obviously, had a huge problems in defence.


I know, this is only spectator's point of view: I want to see more beautiful goals. 
But from a club's perspective the primary goal is the result. No matter how beautiful it is.
That's why Toni Pulis still have his job at West Brom and other commands still 
use corner crosses at training sessions.
  
  
But anyway. It's hard to accept, but it's true: 
> Only **1,27** percents of corners is finished with a goal from a direct cross

So, corner crosses is almost useless. And sometimes are even harmful. Unless you're **West Bromwich**.


Special graph
-------------
There is an Easter Egg here - a special graph, which counts scoring minutes for all 
analysed matches without extra time. The aim is to understand which minute 
of the game is more popular for scoring goals and which is not.  

![Scoring minutes](https://github.com/hesussavas/corners_stats/blob/master/files/images/goals_minutes/goals_minutes.png)

You could see, that the most popular minute is 45' (probably because all goals
scored in the injured time of the first half are mapped to 45th minute in order 
not to interfere with the goals scored in the second time)

It's also clear that the majority of goals is scored during the second time 
of the game. 
