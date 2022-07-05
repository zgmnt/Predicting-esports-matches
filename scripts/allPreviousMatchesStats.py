from bs4 import BeautifulSoup
import requests
import time


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
            time.sleep(0.15)
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


def get_maps_status():
    teamAMap1Win = []
    teamAMap2Win = []
    teamAMap3Win = []
    all_maps_scores = []
    teamAMapWinAllMaps = []
    for i in range(len(matchPagesLinks)): # change to all matches
        soup = url_to_soup(matchPagesLinks[i])
        mapsStatusRaw = soup.find_all(class_="results-team-score") #6
        for j in range(len(mapsStatusRaw)):
            indexBegin = str(mapsStatusRaw[j]).find('team-score')
            indexEnd = str(mapsStatusRaw[j]).find('</div>')
            mapStatus = str(mapsStatusRaw[j])[indexBegin+12: indexEnd] # 12
            all_maps_scores.append( mapStatus )

        if (i % 2):  # error 1015 handle
            time.sleep(0.25)

    for i in range(0,len(all_maps_scores),2 ):
        if all_maps_scores[i].isdigit() and all_maps_scores[i+1].isdigit():
            all_maps_scores[i] = int(all_maps_scores[i])
            all_maps_scores[i+1] = int(all_maps_scores[i+1])
            teamAMapWinAllMaps.append(all_maps_scores[i] > all_maps_scores[i+1])
        else:
            teamAMapWinAllMaps.append(False)

    for i in range(0,len(teamAMapWinAllMaps), 3):
        teamAMap1Win.append(teamAMapWinAllMaps[i])
        teamAMap2Win.append(teamAMapWinAllMaps[i + 1])
        teamAMap3Win.append(teamAMapWinAllMaps[i + 2])

    return teamAMap1Win, teamAMap2Win, teamAMap3Win


def csv_generator_all_results(path_,filename_):
    with open(("%s%s%s" % (path_, filename_, ".csv")), "w", newline="") as file:
        file.write("%s,%s,%s,%s,%s%s"
                   % ("Team A", "Team B", "map1", "map2", "map3", "\n"))
        for i in range(len(map2)):
            file.write("%s,%s,%s,%s,%s\n"% (teamA[i], teamB[i], map1[i], map2[i], map3[i] ))


def csv_generator_team_a_map_status(path_,filename_):
    with open(("%s%s%s" % (path_, filename_, ".csv")), "w", newline="") as file:
        file.write("%s,%s,%s%s"
                   % ("map1", "map2", "map3", "\n"))
        for i in range(len(columnTeamAmap1Win)):
            file.write("%s,%s,%s\n"% (columnTeamAmap1Win[i], columnTeamAmap2Win[i],columnTeamAmap3Win[i]))


pages = 1 # for loop
matchPagesLinks = get_match_pages_results_links("https://www.hltv.org/results", pages)
teamA, teamB = get_teams()
map1, map2, map3 = get_maps()
columnTeamAmap1Win,columnTeamAmap2Win, columnTeamAmap3Win =  get_maps_status()

# generate csv
csv_generator_all_results("..//data//results//", "allPreviousMatchesStats")
csv_generator_team_a_map_status("..//data//results//", "TeamA-map-win-lose-status")
