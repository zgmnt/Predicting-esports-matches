from bs4 import BeautifulSoup
import requests


def convert_url_to_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def export_to_csv(path, columns, teamNames_):
    with open(path, "w") as file:
        file.write("%s, %s" % (columns, "\n"))
        for i in range(len(teamNames_)):
            file.write("%s,%s, %s\n" % (teamNames_[i][0], teamNames_[i][1], isLan[i]))


def generate_team_names(soup_):
    upcomingMatches = soup_.find_all(class_="matchTeam")
    liveMatches = soup_.find_all(class_="liveMatch-container")
    teamNames = []
    team1, team2 = "", ""
    for i in range(len(liveMatches) + 2, len(upcomingMatches)):
        indexBegin = str(upcomingMatches[i]).find("text-ellipsis")
        indexEnd = str(upcomingMatches[i]).find("</div>")
        team = str(upcomingMatches[i])[indexBegin + len('text-ellipsis">'):].replace("</div>", "").replace("\n", "")

        # team 2
        if (i % 2):
            team2 = team
        else:
            team1 = team

        if (i % 2):
            teamNames.append(tuple((team1, team2)))
    return teamNames


def is_matches_lan(soup_):
    isLanSoup = soup_.find_all(class_="upcomingMatch")
    isLanStr = []
    for e in isLanSoup:
        indBegin = str(e).find("lan=")
        indEnd = str(e).find("stars")
        isLanStr.append(str(e)[indBegin + len("lan=") + 1:indEnd - 2])

    return [ele == "true" for ele in isLanStr]


url = "https://www.hltv.org/matches"
soup = convert_url_to_soup(url)
teamNames = generate_team_names(soup)
isLan = is_matches_lan(soup)


export_to_csv("..//data//UpcomingMatches.csv", "Team A,Team B,Lan", teamNames)
