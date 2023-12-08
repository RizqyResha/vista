import re
import json
import webbrowser

import requests
from bs4 import BeautifulSoup

def playmusic(search):
    response = requests.get("https://www.youtube.com/results?search_query="+search).text

    soup = BeautifulSoup(response, 'lxml')
    script = soup.find_all("script")[35]

    json_text = re.search("var ytInitialData = (.+)[,;]{1}", str(script)).group(1)
    json_data = json.loads(json_text)

    content = (
        json_data
        ['contents']['twoColumnSearchResultsRenderer']
        ['primaryContents']['sectionListRenderer']
        ['contents'][0]['itemSectionRenderer']
        ['contents']
    )

    vidIds = []
    for data in content:
        for key, value in data.items():
            if type(value) is dict:
                for k,v in value.items():
                    if k =="videoId" and len(v) == 11:
                        vidIds.append(v)
                        break
    link = "https://www.youtube.com/watch?v="+vidIds[0]
    webbrowser.open_new(link)

playmusic("moonlightbykaliuchis")
