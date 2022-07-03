import csv
from bs4 import BeautifulSoup
import requests

url = "https://www.hltv.org/matches"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
matchesWrapper = soup.find_all(class_="upcomingMatchesWrapper")
matchesDaysUpcoming = soup.find_all(class_="upcomingMatchesSection")
matchDayHeadline = soup.find_all(class_="matchDayHeadline")
matchFrame = soup.find_all(class_="match a-reset")

upcomingMatchesDays = []

for i in range(len(matchDayHeadline)):
    stringLine = str(matchDayHeadline[i])
    indexDateBegin = stringLine.find(">")
    indexDateEnd = stringLine.find("</")
    upcomingMatchesDays.append(stringLine[indexDateBegin + 1: indexDateEnd])

matchedDetailsURLs = []
for i in range(len(matchFrame)):
    indexBegin = str(matchFrame[i]).find("href=")
    indexEnd = str(matchFrame[i]).find('">')
    matchedDetailsURLs.append("https://www.hltv.org/" + str(matchFrame[i])[indexBegin + 6 :indexEnd])

matchedDetailsURLs.pop(0)
pageMatch = requests.get(matchedDetailsURLs[0])
soupMatch = BeautifulSoup(page.content, 'html.parser')

# CHANGE FUNCTION NAME
def find_all_in_soup(ListOfValues, soup):
    matches = []
    teamsRaw = []
    teams = []
    matches = soup.find_all(class_="upcomingMatch")
    for match in matches:
        teamsRaw.append(match.find(class_="matchTeam team1"))
        teamsRaw.append(match.find(class_="matchTeam team2"))

    for teamRaw in teamsRaw:
        teamRaw.find(class_="")



teamNames = soupMatch.find_all(class_="matchTeamName")
teamsInMatchTable = []
teamsInMatchTuples = []

find_all_in_soup(["matchTeam team1"], soup)

for i in range(len(teamNames)):
    indexBegin = str(teamNames[i]).find('">')
    indexEnd = str(teamNames[i]).find("</div>")
    teamsInMatchTable.append(str(teamNames[i])[indexBegin + 2: indexEnd])

for i in range(0, len(teamNames), 2):
    teamsInMatchTuples.append(tuple((teamsInMatchTable[i], teamsInMatchTable[i+1])))

"""
with open("..//data//UpcomingMatches.csv", "w") as file:
    file.write("Team A,Team B\n")
    for tuple_ in teamsInMatchTuples:
        file.write("%s,%s\n" % (tuple_[0], tuple_[1]))
"""
