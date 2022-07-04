from bs4 import BeautifulSoup
import requests
import csv
import time
import re

# TO DO
# check if two team in top 30
# team a score, team b score column
# map column
# map winrate team a and team b column

pages = 3 # some links dont work cause data gaps


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


def get_teams():
    """
    :param pages_amount:
    :return:  teamA, teamB
    """
    teamA_ = []
    teamB_ = []
    teamName = []
    for i in range(len(matchPagesLinks)):
        soup = url_to_soup(matchPagesLinks[i])
        teamsNameRaw = soup.find_all(class_="teamName")
        print(i, "teams")
        if(i%2): # error 1015 handle
            time.sleep(0.25)
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

teamA, teamB = get_teams()


def get_maps():
    mapsRaw = []
    map1_ = []
    map2_ = []
    map3_ = []
    for i in range(len(matchPagesLinks)):
        soup = url_to_soup(matchPagesLinks[i])
        mapsRaw = soup.find_all(class_="mapname")
        print(i, "maps")
        if (i % 2):  # error 1015 handle
            time.sleep(0.25)
        for j in range(len(mapsRaw)):
            indexBegin = str(mapsRaw[j]).find('mapname')
            indexEnd = str(mapsRaw[j]).find('</div>')
            match j:
                case 0:
                    map1_.append(str(mapsRaw[j])[indexBegin + 9:indexEnd])
                case 1:
                    map2_.append(str(mapsRaw[j])[indexBegin + 9:indexEnd])
                case 2:
                    map3_.append(str(mapsRaw[j])[indexBegin + 9:indexEnd])

    return map1_, map2_, map3_


map1, map2, map3 = get_maps()


def all_previous_matches_to_csv(path_,filename_):
    with open(("%s%s%s" % (path_, filename_, ".csv")), "w", newline="") as file:
        file.write("%s,%s,%s,%s,%s%s" % ("Team A", "Team B", "map1", "map2", "map3", "\n"))
        for i in range(len(map2)): # handle blank map2 and map3
            file.write("%s,%s,%s,%s,%s\n" % (teamA[i], teamB[i], map1[i], map2[i], map3[i]))

all_previous_matches_to_csv("..//data//results//", "allPreviousMatchesStats")

