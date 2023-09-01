"""
GSC Match Submission Bot - Mario Kart Table Bot API program
This program takes in a Table Bot ID and transcribes it into storable data for all other programs
Made By: Joey , Alex Keys
"""

#IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from MKOBJECT import Player, Team, Match
from MKOBJECT import PlayerAll, TeamAll
from MKOBJECT import PlayerAPI, MatchAPI, PlayerAPIALL
import csv
import plotly.express as px
import plotly.graph_objs as go
import json
import discord as ds
from discord import app_commands
from discord.ext import commands
from urllib.request import urlopen

#DEFINITION OF MARIO KART WII TRACKS
TRACKS = {"Wii Luigi Circuit": 'LC',
            "Wii Moo Moo Meadows": 'MMM',
            "Wii Mushroom Gorge": 'MG',
            "Wii Toad's Factory": 'TF',
            "Wii Mario Circuit": 'MC',
            "Wii Coconut Mall": 'CM',
            "Wii DK Summit": 'DKS',
            "Wii Wario's Gold Mine": 'WGM',
            "Wii Daisy Circuit": 'DC',
            "Wii Koopa Cape": 'KC',
            "Wii Maple Treeway": 'MT',
            "Wii Grumble Volcano": 'GV',
            "Wii Dry Dry Ruins": 'DDR',
            "Wii Moonview Highway": 'MH',
            "Wii Bowser's Castle": "BCWii",
            "Wii Rainbow Road": 'RR',
            "GCN Peach Beach": 'rPB',
            "DS Yoshi Falls": 'rYF',
            "SNES Ghost Valley 2": 'GV2',
            "N64 Mario Raceway": 'rMR',
            "N64 Sherbet Land": 'rSL',
            "GBA Shy Guy Beach": 'SGB',
            "DS Delfino Square": 'DSDS',
            "GCN Waluigi Stadium": 'rWS',
            "DS Desert Hills": 'rDH',
            "GBA Bowser Castle 3": 'BC3',
            "N64 DK's Jungle Parkway": 'DKJP',
            "GCN Mario Circuit": 'rMC',
            "SNES Mario Circuit 3": 'MC3',
            "DS Peach Gardens": 'rPG',
            "GCN DK Mountain": 'DKM',
            "N64 Bowser's Castle": 'rBC'}
#FUNCTION Read: 
def read(file):

    num = 0
    matches = []

    with open(file, 'r', encoding='utf-8') as infile:

        while True:

            string = infile.readline()

            if string == '':
                break

            else:

                num += 1

                dct = json.loads(string)

                tracks = dct['tracks']

                for i in range(len(tracks)):
                    tracks[i] = TRACKS[tracks[i]]

                teams = dct['teams']
                both = []

                for key in teams:

                    df = pd.DataFrame.from_dict(teams[key])
                    players = []

                    for entry in df['players'].values:

                        player = PlayerAPI(entry['lounge_name'],
                                           sum(entry['gp_scores'][0]),
                                           sum(entry['gp_scores'][1]),
                                           sum(entry['gp_scores'][2]),
                                           entry['total_score'],
                                           entry['mii_name'],
                                           entry['race_scores'],
                                           entry['race_positions'],
                                           entry['flag'],
                                           team=key, num=num, sum=True)

                        players.append(player)

                    gp1 = 0
                    gp2 = 0
                    gp3 = 0

                    for p in players:
                        gp1 += int(p.gp1)
                        gp2 += int(p.gp2)
                        gp3 += int(p.gp3)

                    team = Team(key, gp1, gp2, gp3,
                                teams[key]['table_penalty_str'],
                                int(teams[key]['total_score']),
                                players, num)

                    both.append(team)

                t1t = 'later'
                t2t = 'bruh'

                match = MatchAPI(f'Match #{num}',
                                 both[0],
                                 both[1],
                                 t1t,
                                 t2t,
                                 both[0].score,
                                 both[1].score,
                                 both[0].players + both[1].players,
                                 both[0].score - both[1].score,
                                 num,
                                 tracks)

                matches.append(match)

        return matches

#FUNCTION Summarize:
def summarize(matches):

    player_alls = []
    player_names = []
    p_ids = {}
    p_id = -1

    team_alls = []
    team_names = []
    t_ids = {}
    t_id = -1

    # loops through each match in match list
    for match in matches:

        # creates joint list for all players in match
        both = match.t1.players + match.t2.players

        # loops through each player in combined list
        for player in both:

            # checks if it's the first instance of this player
            if player.name not in player_names:

                # create player_all object for this player
                p_id += 1
                p = PlayerAPIALL(player.name, player.team,
                                 player.gp1, player.gp2, player.gp3, player.points,
                                 player.mii, player.race_scores, player.race_positions,
                                 player.flag, p_id, player.placement, player.num)

                # add id to dictionary, and player to total list
                # saves player name for future updates
                p_ids[p.name] = p_id
                player_alls.append(p)
                player_names.append(player.name)
            else:

                # if player already exists in player_alls
                # find player all object and update it with new match data
                idx = player_names.index(player.name)
                player_alls[idx].update(player)

        # redefines both for new loop, looking at team data now
        both = [match.t1, match.t2]

        # loops for each team
        for team in both:

            # check is team is not already in list
            if team.name not in team_names:

                # creates team_all object
                t_id += 1
                t = TeamAll(team.name, team.gp1, team.gp2,
                            team.gp3, team.pen, team.score,
                            team.players, team.num, t_id)

                # adds id to dict, adds team_all to list
                # saves name for future updates
                t_ids[t.name] = t_id
                team_alls.append(t)
                team_names.append(team.name)
            else:

                # updates team object if already in list
                idx = team_names.index(team.name)
                team_alls[idx].update(team)

            for team_all in team_alls:
                team_all.roster_calc()

    # gets rid of blank ids in id list (it happens idk)
    # p_ids.pop('')
    # t_ids.pop('')

    return player_alls, team_alls, p_ids, t_ids

#PULLING DATA FROM API AND SAVING IT



#FUNCTION Main: Takes table ID's JSON data in, outputs data into a text file for storage
def main(tableID, div):
    #tableID = "1065074404519841873" #Will change into a discord message pull/command pull
    tableBotLink = "http://mkw-table-bot-api.loca.lt/api/json/team_scores/{}?full_details=true".format(tableID)
    response = urlopen(tableBotLink)
    jsonData = json.loads(response.read())

    with open('match_JSON.txt', 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=None)

    with open(f'GSCD{div}.txt', 'a', encoding='utf-8') as allf:
        json.dump(jsonData, allf, ensure_ascii=False, indent=None)
        allf.write("\n")

    matches = read('match_JSON.txt')
    player_alls, team_alls, p_ids, t_ids = summarize(matches)
    print(player_alls)
    print(team_alls)
    print(p_ids)
    print(t_ids)
