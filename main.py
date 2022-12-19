from bs4 import BeautifulSoup as bs
from data import SportData
import threading
import time
import requests
import os
global RUNNING
global CURRENT_SCRAPE

def main():
    global RUNNING
    global CURRENT_SCRAPE

    # Get site data and create BeautifulSoup4 object.
    site_homepage_url = 'https://www.sportscardchecklist.com/'
    site_data = requests.get(site_homepage_url)
    site_soup = bs(site_data.content, 'html.parser')

    # Get list of all sports offered.
    sidebar = site_soup.find('div', {'class': 'left-sidebar'})
    sidebar_list = sidebar.find('ul')
    sidebar_options = sidebar_list.find_all('li')
    sports_pages = []

    CURRENT_SCRAPE = 'SPORTS_PAGES'
    for option in sidebar_options:
        data = SportData(option.get_text(), option.find('a').get('href'))
        sports_pages.append(data)
    CURRENT_SCRAPE = 'YEAR_PAGES'
    # Get list of years of cards of available for each sport
    for sport_page in sports_pages:
        sport_page.get_data()

    CURRENT_SCRAPE = 'SET_PAGES'
    # Get sets for each sport/year
    for sport_page in sports_pages:
        for year_page in sport_page.year_cards_sold:
            year_page.get_data()
            f = open('data.csv', 'a')

            f.write(
                f'{sport_page.sport_name.strip()},{year_page.year},{year_page.url_to_sets_page}\n')
            f.close()

    #CURRENT_SCRAPE = 'WRITE_TO_CSV'
    #for sport_page in sports_pages:
        #for year_page in sport_page.year_cards_sold:
            #for series_page in year_page.sets_released_this.year:

    RUNNING = False

    # TODO: Go through checklists for each sport/year/set
    # TODO: Set up cache for website
    # TODO: Create CSV creation/modification


def printrun():
    global RUNNING
    global CURRENT_SCRAPE
    dots = ''
    while RUNNING:
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        if len(dots) < 3:
            dots += '.'
        else:
            dots = '.'
        print(f'RUNNING{dots}')
        print(CURRENT_SCRAPE)


if __name__ == "__main__":
    global RUNNING
    RUNNING = True
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
