import csv

from bs4 import BeautifulSoup
import re
import requests

url = "https://www.hltv.org/stats/teams/matches/5378/virtuspro?startDate=2018-01-01&endDate=2018-12-31"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
StatsTable = soup.find_all(class_ = "stats-table no-sort")
MapsTable = soup.find_all(class_ = "statsMapPlayed")
detailedResults = soup.find_all(class_ = "statsDetail")

teamAscore = []
teamBscore = []
MatchesStatus = []
Maps = []
# DETAILED SCORE
for i in range(len(detailedResults)):
    mapNameBegin = str(MapsTable[i]).find("<span>")
    mapNameEnd = str(MapsTable[i]).find("</span>")
    Maps.append(str(MapsTable[i])[mapNameBegin + 6: mapNameEnd])
    stringDetailedResults = str(detailedResults[i])
    indexDSBegin = stringDetailedResults.find(">")
    indexDSEnd = stringDetailedResults.find("</")
    score = stringDetailedResults[indexDSBegin+1:indexDSEnd]
    tempA,tempB = score.split(" - ")
    if int(tempA) > int(tempB):
        MatchesStatus.append("W")
    else:
        MatchesStatus.append("L")
    teamAscore.append(tempA)
    teamBscore.append(tempB)

# SAVE TO CSV
filename = "..//data//MatchesResults.csv"
with open(filename, "w", newline="") as file:
    column_names = ["Map", "MatchStatus", "Team A score", "Team B score"]
    thewriter = csv.DictWriter(file, fieldnames=column_names)
    thewriter.writeheader()

    for i in range(len(MatchesStatus)):
        thewriter.writerow({"MatchStatus" : MatchesStatus[i], "Map" : Maps[i], "Team A score" :teamAscore[i],
                            "Team B score": teamBscore[i]})
