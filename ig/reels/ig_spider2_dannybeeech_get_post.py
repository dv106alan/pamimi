from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from util import csv_to_dict_list
from ig_reels_operate import ig_login
import time
import csv
import sys

import os
from dotenv import load_dotenv
load_dotenv()

IG_UserAccount = "dannybeeech"
IG_account = os.getenv("IG_USERNAME")
IG_password = os.getenv("IG_PASSWORD")
IG_list_file_name = os.getenv("IG_LIST_FILE_NAME_1")
IG_post_file_name = os.getenv("IG_POST_FILE_NAME_1")

post_num = 10
if (len(sys.argv) > 1):
    try:
        post_num = int(sys.argv[1])
        print("get post: ",int(sys.argv[1]))
    except Exception as e:
        print(e)

driver = ig_login(IG_account, IG_password)

# Instagram username
username = IG_UserAccount

reel_list = csv_to_dict_list(IG_list_file_name)

field_names = ["url", "likes", "views", "content", 'datetime']

# Write the field name to a CSV file
csvfile = open(IG_post_file_name, 'w', newline='')
writer = csv.DictWriter(csvfile, fieldnames=field_names)
writer.writeheader()
csvfile.close()

for index, reel in enumerate(reel_list):

    csvfile = open(IG_post_file_name, 'a', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    # Navigate to the Instagram profile
    driver.get(f"https://www.instagram.com{reel['key']}")
    time.sleep(3)
    # Get HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    datetime = ""
    date_element = soup.find_all('time', {'class':'xsgj6o6'})
    if (date_element):
        datetime = date_element[0]['datetime']

    # Get HTML content
    html = driver.page_source
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    content_element = soup.find_all('span', class_=lambda x: x and 'x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj' in x)

    good_element = soup.find_all('span', class_=lambda x: x and 'html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu' in x)

    reel_post_list = []
    
    content = ""
    if content_element:
        for element in content_element:
            content += element.getText()

    print(index, " ",reel['key'], " ", datetime)
    print(reel['key'], good_element[0].getText(), reel['value'], datetime)

    writer.writerow({
        "url":f"{reel['key']}",
        "likes":f"{good_element[0].getText()}",
        "views":f"{reel['value']}",
        "content":f"{content}",
        "datetime":f"{datetime}"
        })
    csvfile.close()

    if (index >= post_num):
        break




