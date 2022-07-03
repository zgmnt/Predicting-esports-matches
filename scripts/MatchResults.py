import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

team_stats_csv_path = "..//data//TeamRanking.csv"


def url_to_soup(url_):
    page = requests.get(url_)
    return BeautifulSoup(page.content, 'html.parser')


def link_to_team_stats(ranking_path_):
    ranking_ = pd.read_csv(ranking_path_, sep=",")
    teamIDs = ranking_["teamID"].astype("string")
    teamName = ranking_["name"]
    matches_prefix = "https://www.hltv.org/stats/teams/matches/"
    team_stats_links =[]
    for i in range(len(teamIDs)):
        team_name = teamName[i].replace(".", "").replace(" ", "-").lower()
        fixed_team_name = ("%s%s/%s" % (matches_prefix, teamIDs[i], team_name))
        team_stats_links.append(fixed_team_name)
    return team_stats_links


def get_team_ids():
    teamRanking = pd.read_csv("..//data//TeamRanking.csv", sep=",")
    return teamRanking["teamID"]


def get_team_names():
    teamRanking = pd.read_csv("..//data//TeamRanking.csv", sep=",")
    return teamRanking["name"]


def teams_stats_to_csv(path_,filename_):
    with open(("%s%s%s" % (path_, filename_, ".csv")), "w", newline="") as file:
        column_names = ["Map", "MatchStatus", "Team A score", "Team B score"]
        thewriter = csv.DictWriter(file, fieldnames=column_names)
        thewriter.writeheader()

        for i in range(len(MatchesStatus)):
            thewriter.writerow({"MatchStatus" : MatchesStatus[i], "Map" : Maps[i], "Team A score" :teamAscore[i],
                                "Team B score": teamBscore[i]})


def detailed_score():
    for i in range(len(detailedResults)):
        mapNameBegin = str(MapsTable[i]).find("<span>")
        mapNameEnd = str(MapsTable[i]).find("</span>")
        Maps.append(str(MapsTable[i])[mapNameBegin + 6: mapNameEnd])
        stringDetailedResults = str(detailedResults[i])
        indexDSBegin = stringDetailedResults.find(">")
        indexDSEnd = stringDetailedResults.find("</")
        score = stringDetailedResults[indexDSBegin + 1:indexDSEnd]
        tempA, tempB = score.split(" - ")
        if int(tempA) > int(tempB):
            MatchesStatus.append("W")
        else:
            MatchesStatus.append("L")
        teamAscore.append(tempA)
        teamBscore.append(tempB)


team_stats_links = link_to_team_stats(team_stats_csv_path)
team_names = get_team_names()

for stat_link, team_name in zip(team_stats_links, team_names):
    url = stat_link
    soup = url_to_soup(url)

    StatsTable = soup.find_all(class_="stats-table no-sort")
    MapsTable = soup.find_all(class_="statsMapPlayed")
    detailedResults = soup.find_all(class_="statsDetail")

    teamAscore = []
    teamBscore = []
    MatchesStatus = []
    Maps = []

    teamIDS = get_team_ids()
    detailed_score()
    teams_stats_to_csv("..//data//results//", team_name) # proper name
