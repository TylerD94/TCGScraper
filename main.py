from bs4 import BeautifulSoup as bs
from data import SportData
import threading
import time
import requests
import os


def main():
    # Get site data and create BeautifulSoup4 object.
    site_homepage_url = 'https://www.sportscardchecklist.com/'
    site_data = requests.get(site_homepage_url)
    site_soup = bs(site_data.content, 'html.parser')

    # Get list of all sports offered.
    sidebar = site_soup.find('div', {'class': 'left-sidebar'})
    sidebar_list = sidebar.find('ul')
    sidebar_options = sidebar_list.find_all('li')
    sports_pages = []

    for option in sidebar_options:
        data = SportData(option.get_text(), option.find('a').get('href'))
        sports_pages.append(data)

    # Get list of years of cards of available for each sport
    for sport_page in sports_pages:
        sport_page.get_data()

    # Get sets for each sport/year
    for sport_page in sports_pages:
        for year_page in sport_page.year_cards_sold:
            year_page.get_data()

    # TODO: Go through checklists for each sport/year/set
    # TODO: Set up cache for website
    # TODO: Create CSV creation/modification


def printrun():
    dots = ''
    while True:
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        if len(dots) < 3:
            dots += '.'
        else:
            dots = '.'
        print(f'RUNNING{dots}')


if __name__ == "__main__":
    # main thread handles gathering of data
    # secondary thread prints a constant RUNNING message to the console
    t1 = threading.Thread(target=main)
    t2 = threading.Thread(target=printrun)
    # secondary thread is set as a daemon, any shutdown command will stop all threads
    t2.daemon = True

    t1.start()
    t2.start()

    t1.join(timeout=30)
    t2.join(timeout=30)
