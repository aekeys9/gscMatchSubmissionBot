# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import defaultdict

# constants to be used when S5 table bot data is implemented
COURSES = ['LC', 'MMM', 'MG', 'TF',
           'MC', 'CM', 'DKS', 'WGM',
           'DC', 'KC', 'MT', 'GV',
           'DDR', 'MH', 'BCWii', 'RR',
           'rPB', 'rYF', 'GV2', 'rMR',
           'rSL', 'SGB', 'rDS', 'rWS',
           'rDH', 'BC3', 'rJP', 'GCN MC',
           'MC3', 'rPG', 'DKM', 'rBC']

POINTS = [15, 12, 10, 8, 6, 4, 3, 2, 1, 0]

# ONE INSTANCE of a player (i.e. EmilP in match #7 against XI)
class Player():
    ''' object defining a single instance of a player in a given match

    Attributes:
        name (str): player name
        gp1/gp2/gp3 (int): score in each gp
        points (int): total points scored
        placement (int): placement in war
        team (str): team affiliation
        num (int): match this instance of player played in
        sum (bool): determines if att_clean should be run


    '''

    def __init__(self, name, gp1, gp2, gp3, points, placement=0, team='', num=0, sum=False):

        # creates list for att_clean
        check = [gp1, gp2, gp3, points, placement]

        # setting attributes
        self.name = name
        self.gp1 = gp1
        self.gp2 = gp2
        self.gp3 = gp3
        self.points = points
        self.placement = placement
        self.team = team
        self.num = num

        # runs att_clean if told to
        if sum == False:
            self.att_clean(check)

    def __str__(self):

        return self.name

    def att_clean(self, check):
        ''' cleans data if there are empty spaces

        Arguments:
            check (list): list of inputs from __init__
        '''

        # checks if value can be converted to int
        for i in range(len(check)):
            try:
                check[i] = int(check[i])

            # if value error, change variable to -1
            except ValueError:
                check[i] = -1

        # resets attributes after cleaning
        self.gp1 = check[0]
        self.gp2 = check[1]
        self.gp3 = check[2]
        self.points = check[3]
        self.placement = check[4]

    def spread(self):
        ''' a more in-depth print of player object

        Arguments:
            None
        '''

        return [self.team, self.name, self.gp1, self.gp2, self.gp3,
                self.points, self.placement]

    def sub_parse(self):
        ''' WIP Way to split up subs

        :return:
        '''

        if '/' in self.name:
            name1, name2 = self.name.split('/')

# PLAYER THROUGHOUT SEASON (i.e. all of EmilP's score, places, etc.)
class PlayerAll(Player):
    ''' object that contains all stats a player has in a given season

    Attributes:
        name (str): player name
        team (str): team affiliation
        gp1/gp2/gp3 (list): list of all scores from respective gps
        points (list): list of scores from all matches
        placement (list): list of placements from all matches
        num (list): list of matches player played in
        sum (bool): checks to see if att_clean needs to be run
    '''

    def __init__(self, name, team, gp1, gp2, gp3, points, placement, num, id, sum=True,
                 avg = 0):

        # creates player object
        Player.__init__(self=self, name=name, team=team, gp1=[gp1],
                        gp2=[gp2], gp3=[gp3], points=[points],
                        placement=[placement], num=[num], sum=sum)

        # sets player id
        self.id = id

    def update(self, player):
        ''' updates player_all object with new match info

        Arguments:
            player (player obj): player object from new match
        '''

        # adds new stats to player_all object
        self.num.append(player.num)
        self.gp1.append(player.gp1)
        self.gp2.append(player.gp2)
        self.gp3.append(player.gp3)
        self.points.append(player.points)
        self.placement.append(player.placement)

    def __str__(self):

        t = ''
        for team in self.team:
            t += team + ' '

        return self.name + '\n' + t


class PlayerAPI(Player):

    def __init__(self, name, gp1, gp2, gp3, points,
                 mii, race_scores, race_positions, flag,
                 placement=0, team='', num=0, sum=False,):

        Player.__init__(self=self, name=name, team=team, gp1=gp1,
                        gp2=gp2, gp3=gp3, points=points,
                        placement=[placement], num=num, sum=sum)

        self.mii = mii
        self.race_scores = race_scores
        self.race_positions = race_positions
        self.flag = flag


class PlayerAPIALL(PlayerAPI):

    def __init__(self, name, team, gp1, gp2, gp3, points,
                 mii, race_scores, race_positions, flag, id,
                 placement=0, num=0, sum=True):

        PlayerAPI.__init__(self, name=name, team=team, gp1=[gp1], gp2=[gp2], gp3=[gp3],
                   points=[points], mii=[mii], race_scores=[race_scores],
                   race_positions=[race_positions], flag=flag,
                   placement=[placement], num=[num], sum=sum)

        self.id=id

    def update(self, player):
        ''' updates player_all object with new match info

        Arguments:
            player (player obj): player object from new match
        '''

        # adds new stats to player_all object
        self.num.append(player.num)
        self.gp1.append(player.gp1)
        self.gp2.append(player.gp2)
        self.gp3.append(player.gp3)
        self.points.append(player.points)
        self.placement.append(player.placement)
        self.race_scores.append(player.race_scores)
        self.race_positions.append(player.race_scores)

# ONE INSTANCE of a team (i.e. Daisy playing match #7 against XI)
class Team():
    ''' object that defines one instance of a team playing

    Attributes:
        name (str): team name
        gp1/gp2/gp3 (int): team gp scores
        pen (int): pens on team
        score (int): ending score
        players (list): list of player objects on team
        num (int): match team played
    '''

    def __init__(self, name, gp1, gp2, gp3, pen, score, players=[], num=0):

        # sets attributes
        self.name = name
        self.gp1 = gp1
        self.gp2 = gp2
        self.gp3 = gp3
        self.pen = pen
        self.score = score
        self.players = players
        self.num = num

    def __str__(self):
        string = ""

        for player in self.players:
            string += player.name + ", "

        string = string[:-2]

        return self.name + " Players: " + string

# TEAM THROUGHOUT SEASON (i.e. Daisy overall scores, t-points, etc.)
class TeamAll(Team):
    ''' object that contains total season data for team

    Attributes:
        name (str): team name
        gp1/gp2/gp3 (int): team gp scores
        pen (int): pens on team
        score (int): ending score
        players (list): list of player objects on team
        num (int): match team played
        roster (dict): number of appearances per player
    '''

    def __init__(self, name, gp1, gp2, gp3, pen, score, players, num, id, roster={}):

        # creates team object using inputs
        Team.__init__(self, name=name, gp1=[gp1], gp2=[gp2],
                      gp3=[gp3], pen=[pen], score=[score],
                      players=[players], num=[num])

        # sets team id
        self.id = id

    def update(self, team):
        ''' updates team_all object with new team data

        Arguments:
            team (team object): team data to be added to team_all
        '''

        # add new inputs to team_all lists
        self.num.append(team.num)
        self.gp1.append(team.gp1)
        self.gp2.append(team.gp2)
        self.gp3.append(team.gp3)
        self.score.append(team.score)
        self.players.append(team.players)

    def roster_calc(self):
        ''' Creates roster dictionary

        Arguments:
            None
        '''

        # assigns defaultdict to roster
        roster = defaultdict(lambda: 0)

        # counts player appearances in matches
        for group in self.players:
            for player in group:
                roster[player.name] += 1

        self.roster = roster

        # creates dataframe of player appearances
        df = pd.Series(dict(roster)).sort_values(ascending=False)

        return df

# A match with team and player objects, same as spreadsheet
class Match():

    def __init__(self, name, date, num, t1, t2, t1t, t2t, t1p, t2p, players, dif, id, df=[],
                 perfect=False):

        self.name = name
        self.date = date
        self.num = num
        self.t1 = t1
        self.t2 = t2
        self.t1t = t1t
        self.t2t = t2t
        self.t1p = t1p
        self.t2p = t2p
        self.players = players
        self.dif = dif
        self.id = id
        self.df = self.match_df()

    def __repr__(self):

        print(self.name + ' ' + self.date)
        print(self.match_df())

        return '\n'

    def match_df(self):

        columns = ['Team', 'Player', 'GP1', 'GP2', 'GP3', 'Total', 'Placement']
        full = []
        for player in self.t1.players:
            full.append(player.spread())
        for player in self.t2.players:
            full.append(player.spread())

        df = pd.DataFrame(full, columns=columns)

        return df

class MatchAPI(Match):

    def __init__(self, name, t1, t2, t1t, t2t, t1p, t2p, players, dif, id,
                 races, df=[]):

        Match.__init__(self=self, name=name, date='', num=0, t1=t1, t2=t2,
              t1t=t1t, t2t=t2t, t1p=t1p, t2p=t2p, players=players,
              dif=dif, id=id)

        self.races = races