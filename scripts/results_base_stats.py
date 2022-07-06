import pandas as pd
from bs4 import BeautifulSoup
import requests
import time


def url_to_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def get_links_match_pages(url_, pages_amount):
    offset = 100
    results_links = []
    offset_link = "?offset="
    for i in range(int(pages_amount)):
        soup = url_to_soup(url_)
        results_raw = soup.find(class_="results-holder allres").find_all(class_="result-con")
        for elem in results_raw:
            index_begin = str(elem).find('href="/matches')
            index_end = str(elem).find('<div class="result">')
            prefix = "https://www.hltv.org/"
            results_links.append(prefix + str(elem)[index_begin + 6:index_end - 3])

        url_ = "https://www.hltv.org/results"
        url_ += offset_link + str(offset)
        offset += 100
    return results_links


def get_teams(matches_links):
    team_a = []
    team_b = []
    team_name = []
    for i in range(len(matches_links)):
        soup = url_to_soup(matches_links[i])
        teams_name_raw = soup.find_all(class_="teamName")
        print(i, "teams")
        if i % 2:  # error 1015 handle
            time.sleep(0.5)
        for j in range(2):
            if len(list(teams_name_raw)) != 0:
                team_name = list(teams_name_raw)[j]
            index_begin = str(team_name).find('teamName')
            index_end = str(team_name).find('</div>')
            team_name_fixed = str(team_name)[index_begin + 10: index_end]
            if j % 2:
                team_b.append(team_name_fixed)
            else:
                team_a.append(team_name_fixed)
    return team_a, team_b


def get_maps(matches_links):
    maps = {}
    temp = []
    maps_amount = 0
    maps_played = 0
    for i in range(len(matches_links)):
        soup = url_to_soup(matches_links[i])
        maps_raw = soup.find_all(class_="mapname")
        scores = soup.find_all(class_="results-team-score")

        match len(scores):
            case 2:
                maps_amount = 1
            case 6:
                maps_amount = 3
            case 10:
                maps_amount = 5

        for z in range(0, len(scores), 2):
            index_begin2 = str(scores[z]).find('results-team-score')
            index_end2 = str(scores[z]).find('</div>')
            score_fixed = str(scores[z])[index_begin2 + 20: index_end2]
            if score_fixed.isdigit():
                maps_played += 1

        for j in range(maps_played):
                index_begin = str(maps_raw[j]).find('mapname')
                index_end = str(maps_raw[j]).find('</div>')
                map_fixed = str(maps_raw[j])[index_begin + 9:index_end]
                temp.append(map_fixed)

        maps_played = 0
        maps.update({i+1: list(temp)})
        temp.clear()

        if i % 2:
            time.sleep(0.5)

    return maps


def get_scores(matches_links):
    score_a = []
    score_b = []
    for i in range(len(matches_links)):
        print(i, "scores")
        soup = url_to_soup(matches_links[i])
        scores = soup.find_all(class_="results-team-score")
        for z in range(0, len(scores)):
            index_begin2 = str(scores[z]).find('results-team-score')
            index_end2 = str(scores[z]).find('</div>')
            score_fixed = str(scores[z])[index_begin2 + 20: index_end2]
            if score_fixed.isdigit():
                if z % 2:
                    score_b.append(score_fixed)
                else:
                    score_a.append(score_fixed)

        if i % 2:
            time.sleep(0.5)

    return score_a, score_b


def to_csv_teams_maps(path_, filename_, team_a, team_b, maps):
    with open(("%s%s%s" % (path_, filename_, ".csv")), "w", newline="") as file:
        file.write("%s,%s,%s%s" % ("teamA", "teamB", "map", "\n"))
        for i in range(len(team_a)):
            for j in range(len(list(maps.values())[i])):
                file.write("%s,%s,%s\n" % (team_a[i], team_b[i], list(maps.values())[i][j]))


def to_csv_scores(path_, filename_, score_a, score_b):
    with open(("%s%s%s" % (path_, filename_, ".csv")), "w", newline="") as file:
        file.write("%s,%s%s" % ("scoreTeamA", "scoreTeamB", "\n"))
        for i in range(len(score_a)):
            file.write("%s,%s\n" % (score_a[i], score_b[i]))


URL = "https://www.hltv.org/results"
RESULTS_PATH = "..//data//results//"
PAGES_AMOUNT = 2
MATCHES_LINKS = get_links_match_pages(URL, PAGES_AMOUNT)


TEAM_A, TEAM_B = get_teams(MATCHES_LINKS)
MAPS = get_maps(MATCHES_LINKS)
SCORE_A, SCORE_B = get_scores(MATCHES_LINKS)
# generate csv
to_csv_teams_maps(RESULTS_PATH, "results_teams_maps", TEAM_A, TEAM_B, MAPS)
to_csv_scores(RESULTS_PATH, "results_scores", SCORE_A,SCORE_B)
# concat
TEAMS_MAPS = pd.read_csv("..//data//results//results_teams_maps.csv.")
SCORES = pd.read_csv("..//data//results//results_scores.csv.")
RESULTS = pd.concat([TEAMS_MAPS, SCORES], axis=1)
RESULTS.to_csv("..//data//results//basic_stats.csv.")
