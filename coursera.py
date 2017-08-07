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


def get_course_info(course_url):
    try:
        course_html = requests.get(course_url).content
    except requests.exceptions.ConnectionError as error:
        print(error)
    else:
        soup = BeautifulSoup(course_html, 'lxml')
        
        course_name = soup.find("h1").string
        course_language = soup.find('div', class_='language-info').contents[0].contents[1]
        
        try:
            course_commitment = soup.find('span', class_='td-title', string='Commitment').parent.parent.contents[1].string
        except AttributeError:
            course_commitment = 'No info'
        
        try:
            course_avg_rating = re.sub('(Rated\s)|(\sout\sof\s5\sof\s)',
                                '',
                                soup.find('div', class_='ratings-text headline-2-text').contents[0].contents[1])
        except AttributeError:
            course_avg_rating = 'No rating'

        course_nearest_start = re.sub("Starts\s",
                               '',
                               soup.find("div", class_='startdate rc-StartDateString caption-text').contents[0].string)
        
        print(".", end="")
        return course_name, course_language, course_commitment, course_avg_rating,     course_nearest_start


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
    max_courses = 50
    for url in courses_urls[:max_courses]:
        courses_data.append(get_course_info(url))
    
    output_courses_info_to_xlsx(courses_data, filepath=filename)


if __name__ == '__main__':
    main()
