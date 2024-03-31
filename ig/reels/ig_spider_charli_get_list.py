from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
from util import dict_to_csv
from ig_reels_operate import ig_login, ig_reels_view, ig_reel_get_url_viewcount

import os
from dotenv import load_dotenv
load_dotenv()

IG_UserAccount = "coindevanity"
IG_account = os.getenv("IG_USERNAME")
IG_password = os.getenv("IG_PASSWORD")
IG_list_file_name = os.getenv("IG_LIST_FILE_NAME_2")

# print(IG_account, IG_password, IG_list_file_name)

if __name__ == "__main__":
    post_num = 30
    if (len(sys.argv) > 1):
        try:
            post_num = int(sys.argv[1])
            print("get post: ",int(sys.argv[1]))
        except Exception as e:
            print(e)

    print("Log in...")
    driver = ig_login(IG_account, IG_password)
    print("Go reels page...")
    ig_reels_view(driver, IG_UserAccount)

    continues = True
    view_count = {}

    new_len = 0
    old_len = 0

    print("Get reels list...")
    # Get IG reels url list
    while (continues):
        for x in range(1, 2):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
        
        # Get HTML content
        html = driver.page_source
        
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        reel_posts = soup.find_all('a', {"class":"x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"})
        
        for post in reel_posts:
            url, count = ig_reel_get_url_viewcount(post)
            if url is not None:
                view_count[f"{url}"] = count

        # check if no more to add, then stop process
        new_len = len(view_count)
        if (new_len == old_len):
            break
        
        old_len = new_len
        
        print(new_len)

        index = len(view_count)
        if (index >= post_num):
            break

    print("save to csv...")
    dict_to_csv(view_count, IG_list_file_name)





