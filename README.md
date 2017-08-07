# Coursera Dump

This script will get random 50 courses from [Coursera xml feed](https://www.coursera.org/sitemap~www~courses.xml), then parse some data directly from coursera webpage using BeautifulSoup4 and, finally, will create .xlsx file with parsed data.

Anton Demkin, 2017

# Installation
Script requires Python 3. To install additional modules run this terminal command from folder with this script:
```
pip3 install -r requirements.txt
```

# How to use

Simply run this script with output excel file as single argument. Script will automatically do the rest. Excel file will be created in same folder with this script.
```
python3 coursera.py coursera.xlsx 
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
