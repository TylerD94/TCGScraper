from bs4 import BeautifulSoup as bs
import requests

class SportData:
    year_cards_sold = []

    def __init__(self, sport_name, url_to_checklist_page):
        self.sport_name = sport_name
        self.url_to_checklist_page = url_to_checklist_page

    def get_data(self):
        page_data = requests.get(self.url_to_checklist_page)
        page_soup = bs(page_data.content, 'html.parser')
        year_container = page_soup.find('div', {'class': 'tab-content'})
        years = year_container.find_all('li')
        for year in years:
            data = YearData(year.get_text(), year.find('a').get('href'))
            self.add_data(data)

    def add_data(self, yeardata):
        self.year_cards_sold.append(yeardata)


class YearData:
    sets_released_this_year = []

    def __init__(self, year, url_to_sets_page):
        self.year = year
        self.url_to_sets_page = url_to_sets_page

    def get_data(self):
        page_data = requests.get(self.url_to_sets_page)
        page_soup = bs(page_data.content, 'html.parser')
        set_container = page_soup.find('div', {'class': 'tab-content'})
        sets = set_container.find_all('li')
        for set in sets:
            data = SeriesData(set.get_text(), set.find('a').get('href'))
            self.add_data(data)

    def add_data(self, series):
        self.sets_released_this_year.append(series)


class SeriesData:
    def __init__(self, set_name, url_to_checklist_page):
        self.set_name = set_name
        self.url_to_checklist_page = url_to_checklist_page


class CardData:
    def __init__(self, set_name, player_name, team,):
        self.set_name = set_name
        self.player_name = player_name
        self.team = team
