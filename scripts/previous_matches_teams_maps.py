from bs4 import BeautifulSoup
import requests
import time


def url_to_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def get_links_match_pages(url_, pages_amount):
    offset = 100
    results_links = []
    offsetLink = "?offset="
    offsetMax = pages_amount * offset
    for i in range(int(pages_amount)):
        resultsRaw = url_to_soup(url_).find_all(class_="result-con")
        for elem in resultsRaw:
            indexBegin = str(elem).find('href="/matches')
            indexEnd = str(elem).find('<div class="result">')
            prefix = "https://www.hltv.org/"
            results_links.append(prefix + str(elem)[indexBegin + 6:indexEnd - 3])
        url_ = "https://www.hltv.org/results"
        url_ += offsetLink + str(offset)
        offset += 100
    return results_links


def get_teams(matches_links):
    teamA_ = []
    teamB_ = []
    teamName = []
    for i in range(len(matches_links)):
        soup = url_to_soup(matches_links[i])
        teamsNameRaw = soup.find_all(class_="teamName")
        print(i, "teams")
        if (i % 2):  # error 1015 handle
            time.sleep(0.15)
        for j in range(2):
            if len(list(teamsNameRaw)) != 0:
                teamName = list(teamsNameRaw)[j]
            indexBegin = str(teamName).find('teamName')
            indexEnd = str(teamName).find('</div>')
            teamnameFixed = str(teamName)[indexBegin + 10: indexEnd]
            if j % 2:
                teamB_.append(teamnameFixed)
            else:
                teamA_.append(teamnameFixed)
    return teamA_, teamB_


def get_maps(matches_links):
    mapsRaw = []
    map1_ = []
    map2_ = []
    map3_ = []
    for i in range(len(matches_links)):
        soup = url_to_soup(matches_links[i])
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


def get_maps_status(matches_links):
    teamAMap1Win = []
    teamAMap2Win = []
    teamAMap3Win = []
    all_maps_scores = []
    teamAMapWinAllMaps = []
    for i in range(len(matches_links)):  # change to all matches
        soup = url_to_soup(matches_links[i])
        mapsStatusRaw = soup.find_all(class_="results-team-score")  # 6
        for j in range(len(mapsStatusRaw)):
            indexBegin = str(mapsStatusRaw[j]).find('team-score')
            indexEnd = str(mapsStatusRaw[j]).find('</div>')
            mapStatus = str(mapsStatusRaw[j])[indexBegin + 12: indexEnd]  # 12
            all_maps_scores.append(mapStatus)

        if (i % 2):  # error 1015 handle
            time.sleep(0.25)

    for i in range(0, len(all_maps_scores), 2):
        if all_maps_scores[i].isdigit() and all_maps_scores[i + 1].isdigit():
            all_maps_scores[i] = int(all_maps_scores[i])
            all_maps_scores[i + 1] = int(all_maps_scores[i + 1])
            teamAMapWinAllMaps.append(all_maps_scores[i] > all_maps_scores[i + 1])
        else:
            teamAMapWinAllMaps.append(False)

    for i in range(0, len(teamAMapWinAllMaps), 3):
        teamAMap1Win.append(teamAMapWinAllMaps[i])
        teamAMap2Win.append(teamAMapWinAllMaps[i + 1])
        teamAMap3Win.append(teamAMapWinAllMaps[i + 2])

    return teamAMap1Win, teamAMap2Win, teamAMap3Win


def to_csv_teams_maps(page, path_, filename_, map1, map2, map3, team_a, team_b):
    with open(("%s%s%s%s%s" % (path_, filename_,"_p_", page, ".csv")), "w", newline="") as file:
        file.write("%s,%s,%s,%s,%s%s" % ("Team A", "Team B", "map1", "map2", "map3", "\n"))
        for i in range(len(map2)-1):
            file.write("%s,%s,%s,%s,%s\n" % (team_a[i], team_b[i], map1[i], map2[i], map3[i]))


def to_csv_team_a_map_status(page, path, filename, map1, map2, map3):
    with open(("%s%s%s%s%s" % (path, filename,"_p_",page, ".csv")), "w", newline="") as file:
        file.write("%s,%s,%s%s" % ("map1", "map2", "map3", "\n"))
        for i in range(len(map1)-1):
            file.write("%s,%s,%s\n" % (map1[i], map2[i], map3[i]))


URL = "https://www.hltv.org/results"
PAGES_AMOUNT = 3  # page-csv file, then join tables
for i in range(PAGES_AMOUNT):

    MATCHES_LINKS = get_links_match_pages(URL, PAGES_AMOUNT)
    TEAM_A, TEAM_B = get_teams(MATCHES_LINKS)
    MAP1, MAP2, MAP3 = get_maps(MATCHES_LINKS)
    COLUMN_TEAM_A_MAP_1_STATUS, COLUMN_TEAM_A_MAP_2_STATUS, COLUMN_TEAM_A_MAP_3_STATUS = get_maps_status(MATCHES_LINKS)


    # generate csv
    RESULTS_PATH = "..//data//results//"
    to_csv_teams_maps(PAGES_AMOUNT,RESULTS_PATH, "previous-matches-stats", MAP1, MAP2, MAP3, TEAM_A, TEAM_B)
    to_csv_team_a_map_status(PAGES_AMOUNT,RESULTS_PATH,"team-A-map-win-status",
                             COLUMN_TEAM_A_MAP_1_STATUS, COLUMN_TEAM_A_MAP_2_STATUS, COLUMN_TEAM_A_MAP_3_STATUS)
