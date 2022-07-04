from bs4 import BeautifulSoup
import requests
import csv

# TO DO
# check if two team in top 30
# team a, team b column
# team a score, team b score column
# map column
# map winrate team a and team b column

pages = 6

def url_to_soup(url_):
    page = requests.get(url_)
    return BeautifulSoup(page.content, 'html.parser')


def get_match_pages_results_links(url_,amount_pages):
    offset = 100
    resultsLinks_ = []
    offsetLink = "?offset="
    offsetMax = amount_pages*offset
    for i in range(int(amount_pages)):
        resultsRaw = url_to_soup(url_).find_all(class_="result-con")
        for elem in resultsRaw:
            indexBegin = str(elem).find('href="/matches')
            indexEnd = str(elem).find('<div class="result">')
            prefix = "https://www.hltv.org/"
            resultsLinks_.append(prefix + str(elem)[indexBegin + 6:indexEnd - 3])
        url_ = "https://www.hltv.org/results"
        url_ += offsetLink+str(offset)
        offset += 100
    return resultsLinks_

matchPagesLinks = get_match_pages_results_links("https://www.hltv.org/results", pages)


def get_teams(pages_amount):
    """
    :param pages_amount:
    :return:  teamA, teamB
    """
    teamA_ = []
    teamB_ = []
    for i in range(len(matchPagesLinks)):
        soup = url_to_soup(matchPagesLinks[i])
        teamsNameRaw = soup.find_all(class_="teamName")
        for j in range(2):
            if len(list(teamsNameRaw)) != 0:
                teamName = list(teamsNameRaw)[j]
            indexBegin = str(teamName).find('teamName')
            indexEnd = str(teamName).find('</div>')
            teamnameFixed = str(teamName)[indexBegin + 10: indexEnd]
            if j%2:
                teamB_.append(teamnameFixed)
            else:
                teamA_.append(teamnameFixed)
    return teamA_, teamB_


teamA, teamB = get_teams(pages)


def all_previous_matches_to_csv(path_,filename_):
    with open(("%s%s%s" % (path_, filename_, ".csv")), "w", newline="") as file:
        file.write("%s,%s%s" % ("Team A", "Team B", "\n"))
        for i in range(len(teamA)):
            file.write("%s,%s\n" % (teamA[i], teamB[i]))


all_previous_matches_to_csv("..//data//results//", "allPreviousMatchesStats")
