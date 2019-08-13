import requests
from bs4 import BeautifulSoup
import re
import scraperwiki

url = 'https://www.fussballgucken.info/fussball-heute'
covs = []

try:
    page_response = requests.get(url, timeout=5)

    if page_response.status_code == 200:
        page_content = BeautifulSoup(page_response.content, 'lxml')

        standings_table = page_content.find('div', attrs={'class': 'match-table'})
        date = [gl.get_text() for gl in standings_table.select('.row.date')]
        kick_off = [tm.get_text() for tm in standings_table.select('.time')]
        leagues = standings_table.findAll('a', href=re.compile("wettbewerb"))
        home_team = [tl.get_text() for tl in standings_table.select('.match .col-xs-5.only-top-padding.text-right')]
        away_team = [tr.get_text() for tr in standings_table.select('.match .col-xs-5.only-top-padding.text-left')]

        coverages = [cv.get_text() for cv in standings_table.select('.coverages')]
        for cov in coverages:
            covs.append(cov[:15])

        games = [gm.get_text() for gm in standings_table.select('.row.game')]

        for x, game in enumerate(games):
            # content.append(Match(date, leagues[x].text.strip(), kick_off[x], home_team[x], away_team[x], (coverages[x])))

            content = {"leagues": leagues[x].text.strip(), "kickoff": kick_off[x], "home_team": home_team[x],
                       "away_team": away_team[x], "coverages": covs[x], "date": ""}

            scraperwiki.sql.save(['home_team'], data=content)

    else:
        print(page_response.status_code)

except requests.Timeout as e:
    print('Timeout occurred for requested page: ' + url)
    print(str(e))

