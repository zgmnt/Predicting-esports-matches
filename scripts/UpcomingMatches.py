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


with open("..//data//UpcomingMatches.csv", "w") as file:
    file.write("Team A,Team B\n")
    for tuple_ in teamNames:
        file.write("%s,%s\n" % (tuple_[0], tuple_[1]))
