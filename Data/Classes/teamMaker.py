from Data.Classes.Team import *
import json
from dataclasses import asdict
import sys
def makeTeams():
    team1 = Team()
    team1.teamName = "home"
    team2 = Team()
    team2.teamName = "away"
    nList = ["Jerry Matthews", "Jacob Foley", "Xavier Dyer", "Aron Hunter", "Aditya Kumar",
             "Jai Kata", "Julian Collado", "Yousif Alqaysi", "Keith Shaw", "Reid O'Neill", "Jordan Charles",
             "Omer Reed", "Brendan Smith", "Dylan Cannon", "Pablo Wheeler",
             "Frank Wise", "Dakota Montoya", "Austin Solis"]  # list of all player names for both teams
    pNums = [42, 4, 21, 24, 42, 23, 14, 3, 44, 6, 31, 1, 12, 15, 9, 27, 2,
             7]  # list of all player numbers for both teams
    sList = [(99, 52, 99, 90), (55, 99, 96, 90), (65, 80, 99, 96), (58, 75, 68, 99), (99, 45, 99, 97), (85, 85, 85, 85),
             (99, 99, 99, 99),
             (50, 50, 50, 50), (50, 95, 99, 96), (99, 52, 99, 90), (55, 99, 96, 90), (65, 80, 99, 96), (58, 75, 68, 99),
             (99, 45, 99, 97),
             (85, 85, 85, 85), (99, 99, 99, 99), (50, 50, 50, 50), (50, 95, 99, 96)]
    posList = ["first", "second", "short", "third", "catch", "pitch", "LF", "CF", "RF"]

    for i in range(9):
        player = Player()
        player.name = nList[i]
        player.num = pNums[i]
        player.bStat, player.pStat, player.fStat, player.sStat = sList[i]
        player.team = "home"
        #player.bStat = sList[i][0]
        #player.pStat = sList[i][1]
        #player.fStat = sList[i][2]
        #player.sStat = sList[i][3]
        team1.roster.append(player)

    for i in range(9, len(nList)):
        player = Player()
        player.name = nList[i]
        player.num = pNums[i]
        player.bStat, player.pStat, player.fStat, player.sStat = sList[i]
        player.team = "away"
        # player.bStat = sList[i][0]
        # player.pStat = sList[i][1]
        # player.fStat = sList[i][2]
        # player.sStat = sList[i][3]
        team2.roster.append(player)
    with open('Data/Assets/homeTeam.json', 'w') as H:
        json.dump(asdict(team1), H, indent=4)
    with open('Data/Assets/awayTeam.json', 'w') as A:
        json.dump(asdict(team2), A, indent=4)

    print(f'Home Team: {team1}')
    print(f'Away Team: {team2}')

makeTeams()