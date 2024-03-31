from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re
import time
import csv


def get_video_urls(channel_url, num_videos=31): #抓取前31筆影片網址
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(channel_url)
    time.sleep(5)
    page_source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_source, 'html.parser')
    video_elements = soup.find_all("a", id="video-title-link")

    video_urls = []
    for element in video_elements[:num_videos]:
        video_urls.append(element.get('href'))

    return video_urls

def bottom (driver): #最大化、等3秒、點擊按鈕(瀏覽資訊)
    driver.maximize_window()
    time.sleep(3)
    try:
        button = driver.find_element(By.ID, 'expand')
        button.click()
    except Exception as e:
        print("按鈕點擊錯誤:", e)

def scroll_down(driver): #滾動頁面4次 每次等待2秒
    for _ in range(4):
        time.sleep(2)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        

def find_first_message(messages): #找到第一則留言數 第一則留言數不為空
    for msg in messages:
        if msg.text.strip():
            return msg.text.strip()
        
def extract_number(text): #提取數字  EX.觀看次數:1234次  -> 1234
    numbers = re.findall(r'\d+', text)
    number_str = ''.join(numbers)
    return int(number_str)


def get_video_info(video_urls, options):   #抓取影片資訊 並存成list
    video_info_list = []
    for video_url in video_urls:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(f"https://www.youtube.com{video_url}")
        time.sleep(3)
        
        bottom(driver)
        scroll_down(driver)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        title_tag = soup.find("h1", class_="style-scope ytd-watch-metadata")
        title_text = title_tag.text.strip() 
        views = soup.find_all("span" , class_="style-scope yt-formatted-string bold")
        views_text = views[0].text.strip()
        views_number = extract_number(views_text) 
        date = soup.find_all("span" , class_="style-scope yt-formatted-string bold")
        date_text = date[2].text.strip() 
        like = soup.find('div', class_='YtwFactoidRendererFactoid')
        like_text = like.text.strip() 
        message = soup.find_all('span', class_='style-scope yt-formatted-string', dir='auto')
        message_text = find_first_message(message)
        video_info_list.append({'標題': title_text, '觀看次數': views_number, '日期': date_text, '喜歡次數': like_text[:-4], '留言次數': message_text})
        
        driver.quit()

    return video_info_list

def write_video_info_to_csv(video_info, file_path): #將list存成csv檔
    fieldnames = ['標題', '觀看次數', '日期', '喜歡次數', '留言次數']
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for idx, info in enumerate(video_info, start=1):
            writer.writerow(info)
            print(f"已成功寫入第 {idx} 筆資料到 CSV 文件中。")

    print("所有資料已成功寫入到 CSV 文件中。")


