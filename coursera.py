from xml.etree import ElementTree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests
import random
import re
import sys

coursera_xml_url = 'https://www.coursera.org/sitemap~www~courses.xml'


def get_courses_list():
    try:
        courses_data = requests.get(coursera_xml_url).content
    except requests.exceptions.ConnectionError as error:
        print(error)
    else:
        element_tree_data = ElementTree.fromstring(courses_data)
        return [element[0].text for element in element_tree_data]

def load_html_from_url(url):
    try:
        raw_html = requests.get(url).content
    except requests.exceptions.ConnectionError as error:
        print(error)
    else:
        return raw_html

def get_course_info(course_html):

    soup = BeautifulSoup(course_html, 'lxml')
    
    title = soup.find("h1").string
    language = soup.find('div', class_='language-info').contents[0].contents[1]
    
    try:
        commitment = soup.find('span', class_='td-title', string='Commitment').parent.parent.contents[1].string
    except AttributeError:
        commitment = 'No info'
    
    try:
        rating_soup = soup.find('div', class_='ratings-text headline-2-text').contents[0].contents[1]
    except AttributeError:
        rating = 'No rating'
    else:
        # filter out anything but pure rating, maybe use as digit in future
        rating = re.sub('(Rated\s)|(\sout\sof\s5\sof\s)', '', rating_soup)
    
    start_soup = soup.find("div", class_='startdate rc-StartDateString caption-text').contents[0].string
    start = re.sub("Starts\s", '', start_soup)
    
    return title, language, commitment, rating, start


def output_courses_info_to_xlsx(filedata, filepath):
    work_book = Workbook()
    excel_table = work_book.active
    
    for row in filedata:
        excel_table.append(row)
    
    work_book.save(filepath)


def main():
    if len(sys.argv) < 2:
        print("Usage: coursera.py [filename]")
        exit()
    
    filename = sys.argv[1]
    courses_urls = get_courses_list()
    random.shuffle(courses_urls)
    courses_data = []
    print("Working... may take some time.")
    max_courses = 3
    for url in courses_urls[:max_courses]:
        courses_data.append(get_course_info(load_html_from_url(url)))
    
    output_courses_info_to_xlsx(courses_data, filepath=filename)
    print('Done! File {} created.'.format(filename))


if __name__ == '__main__':
    main()
