import csv
from bs4 import BeautifulSoup
import requests

url = "https://www.hltv.org/ranking/teams/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


def get_team_ids(soup_):
    teamIDsRaw = soup_.find_all(class_="moreLink")
    teamIDs = []
    for e in teamIDsRaw:
        indexBegin = str(e).find("details/")
        indexEnd = str(e).find("HLTV")
        teamID = (str(e)[indexBegin: indexEnd]) \
            .replace('">Ranking details</a', "").replace('details/', "")
        teamIDs.append(teamID)

    return list(filter(lambda e: e != "", teamIDs))


team_ids = get_team_ids(soup)

rankingTable = soup.find_all(class_="ranking")
rankingTableTeams = soup.find_all(class_="ranked-team standard-box")
position = soup.find_all(class_="position")
name = soup.find_all(class_="name")
positionsAssociatedNames = {}
offsetDecimal = 2
for i in range(len(rankingTableTeams)):
    stringPos = str(rankingTableTeams[i])
    indexPos = stringPos.find("#")
    indexName = str(name[i]).find("name")
    indexNameEnd = str(name[i]).find("</span>")
    key = str(name[i])[indexName+6: indexNameEnd]
    if i > 8:
        teamPosition = stringPos[indexPos+1: indexPos + offsetDecimal+1]
    else:
        teamPosition = stringPos[indexPos+1: indexPos + offsetDecimal]

    positionsAssociatedNames.update({key : teamPosition})





with open("..//data//TeamRanking.csv", "w") as file:
    file.write("name,position,teamID\n")
    for key, team_id in zip(positionsAssociatedNames.keys(), team_ids):
        file.write("%s,%s,%s\n" % (key, positionsAssociatedNames[key], team_id))