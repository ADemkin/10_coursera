from lxml import etree
from io import StringIO, BytesIO

from xml.etree import ElementTree as et

from bs4 import BeautifulSoup

import openpyxl
import requests

import random

import collections

import re

coursera_xml_url = 'https://www.coursera.org/sitemap~www~courses.xml'


def get_courses_list():
    try:
        data = requests.get(coursera_xml_url).content
    except requests.exceptions.ConnectionError as error:
        print(error)
    else:
        et_data = et.fromstring(data)
        return [element[0].text for element in et_data]


def get_course_info(course_url):
    # TODO: get name, lang, nearest start, learning weeks, avg score
    # TODO: for course in courses_url
    course = course_url
    try:
        course_html = requests.get(course).content
    except requests.exceptions.ConnectionError as error:
        print(error)
    else:
        # print(course_html)
        soup = BeautifulSoup(course_html, 'lxml')
        print("Url: {}".format(course))
        
        name = soup.find("h1").string  # working!
        print("Name: {}".format(name))
        # language = soup.find_all(attrs={'data-reactid':'165'})[0].string
        language = soup.find('div', class_='language-info').contents[0].contents[1]
        
        print("Lang: {}".format(language))
        # commitment = soup.find_all(attrs={'data-reactid':158})[0].string  # working!
        
        # commitment is not always present
        try:
            commitment = soup.find('span', class_='td-title', string='Commitment').parent.parent.contents[1].string
        except AttributeError:
            commitment = 'No info'
            
        print("Comm: {}".format(commitment))
        
        # avg_rating = soup.find(string=re.compile('(\d(\.\d)?(?=\sout\sof\s5\sof\s))'))
        #avg_rating = soup.find('div', class_='ratings-text headline-2-text').contents[0].contents[1]
        
        # some courses have no ratings
        try:
            avg_rating = re.sub('(Rated\s)|(\sout\sof\s5\sof\s)',
                                '',
                                soup.find('div', class_='ratings-text headline-2-text').contents[0].contents[1])
        except AttributeError:
            avg_rating = 'No rating for this course'
            
        print("Avg rating: {}".format(avg_rating))
        

        nearest_start = re.sub("Starts\s",
                               '',
                               soup.find("div",
                                         class_='startdate rc-StartDateString caption-text').contents[0].string)
        print("Start: {}".format(nearest_start))
        print("")


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    courses_urls = get_courses_list()
    print("Total courses: {}".format(len(courses_urls)))
    random.shuffle(courses_urls)  # TODO: maybe remove this
    # print(courses_urls)
    # courses_urls = ['https://www.coursera.org/learn/infrastructure-investing']
    # courses_urls = ['https://www.coursera.org/specializations/excel-mysql']
    for url in enumerate(courses_urls):
        print(url[0])
        get_course_info(url[1])
