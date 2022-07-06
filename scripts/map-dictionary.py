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
        results_raw = url_to_soup(url_).find_all(class_="result-con")
        for elem in results_raw:
            index_begin = str(elem).find('href="/matches')
            index_end = str(elem).find('<div class="result">')
            prefix = "https://www.hltv.org/"
            results_links.append(prefix + str(elem)[index_begin + 6:index_end - 3])
        url_ = "https://www.hltv.org/results"
        url_ += offset_link + str(offset)
        offset += 100
    return results_links


def get_maps(matches_links):
    maps = {}
    temp = []
    for i in range(4):
        soup = url_to_soup(matches_links[i])
        maps_raw = soup.find_all(class_="mapname")
        scores = soup.find_all(class_="results-team-score")
        for z in range(4,len(scores),2): # - = bo2, digit = bo3
            index_begin2 = str(scores[z]).find('results-team-score')
            index_end2 = str(scores[z]).find('</div>')
            score_fixed = str(scores[z])[index_begin2 + 20: index_end2]
            if score_fixed.isdigit():
                maps_amount = 3
            else:
                maps_amount = 2

            for j in range(maps_amount):
                index_begin = str(maps_raw[j]).find('mapname')
                index_end = str(maps_raw[j]).find('</div>')
                map_fixed = str(maps_raw[j])[index_begin + 9:index_end]
                temp.append(map_fixed)

        maps.update({i+1: list(temp)})
        temp.clear()

        if i % 2:
            time.sleep(0.5)

    return maps


URL = "https://www.hltv.org/results"
PAGES_AMOUNT = 1
MATCHES_LINKS = get_links_match_pages(URL, PAGES_AMOUNT)
MAPS = get_maps(MATCHES_LINKS)

print(MAPS)
