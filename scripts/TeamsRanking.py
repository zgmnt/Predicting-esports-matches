import csv
from bs4 import BeautifulSoup
import requests

url = "https://www.hltv.org/ranking/teams/"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
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
    file.write("name,position\n")
    for key in positionsAssociatedNames.keys():
        file.write("%s,%s\n" % (key, positionsAssociatedNames[key]))