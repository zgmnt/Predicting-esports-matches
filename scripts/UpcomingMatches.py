from bs4 import BeautifulSoup
import requests


url = "https://www.hltv.org/matches"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

upcomingMatches = soup.find_all(class_="matchTeam")
liveMatches = soup.find_all(class_="liveMatch-container")

teamNames = []
team1, team2 = "", ""
for i in range(len(liveMatches)+2, len(upcomingMatches)):
    indexBegin = str(upcomingMatches[i]).find("text-ellipsis")
    indexEnd = str(upcomingMatches[i]).find("</div>")
    team = str(upcomingMatches[i])[indexBegin + len('text-ellipsis">'):].replace("</div>", "").replace("\n", "")

    # team 2
    if(i%2):
        team2 = team
    else:
        team1 = team

    if (i % 2):
        teamNames.append(tuple((team1, team2)))


isLanSoup = soup.find_all(class_ = "upcomingMatch")
isLanStr = []
for e in isLanSoup:
    indBegin = str(e).find("lan=")
    indEnd = str(e).find("stars")
    isLanStr.append(str(e)[indBegin + len("lan=")+1:indEnd-2])

isLan = [ele == "true" for ele in isLanStr]

with open("..//data//UpcomingMatches.csv", "w") as file:
    file.write("Team A,Team B, Lan\n")
    for i in range(len(teamNames)):
        file.write("%s,%s, %s\n" % (teamNames[i][0], teamNames[i][1], isLan[i]))