from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from util import dict_to_csv

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("headless")

service = Service(ChromeDriverManager().install())
driver = any

def ig_login (account, pwd):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=service, options = options)

    driver.get("https://www.instagram.com/")

    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    pwdstr = pwd
    usnstr = account
    username.clear()
    password.clear()
    username.send_keys(usnstr)
    password.send_keys(pwdstr)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)

    return driver

def ig_reels_view(driver, account):
    # Instagram username
    username = account

    # Navigate to the Instagram profile
    driver.get(f"https://www.instagram.com/{username}/reels")

    # Wait for the reel section to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'reel')]/parent::div"))
    )
    time.sleep(5)

def ig_reel_get_url_viewcount(post) -> tuple:
    count = post.find_all('span', {'class':'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xl565be x1s688f x9bdzbf x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj'})
    
    if count:
        value = f"{count[0].getText()}"
        # change view count words to digit
        if (value[-1:] == 'K'):
            numeric_part = float(value[:-1])
            integer_value = int(numeric_part * 1000)
            value = str(integer_value)
        elif (value[-1:] == 'M'):
            numeric_part = float(value[:-1])
            integer_value = int(numeric_part * 1000000)
            value = str(integer_value)
        else:
            integer_value = int(value.replace(',', ''))
            value = str(integer_value)

        return f"{post.get('href')}", f"{value}"
    else:
        return None, None