from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import csv


def get_facebook_data(email: str, password: str, chrome_url: str, Danny_url: str) -> list[str]:
    service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get(chrome_url)
    time.sleep(1)

    email = driver.find_element(By.ID, "email").send_keys(email)
    password = driver.find_element(By.ID, "pass").send_keys(password)
    login = driver.find_element(By.NAME, "login")
    login.submit()
    time.sleep(1)

    driver.get(Danny_url)
    time.sleep(1)  # 等待頁面加載完成
    
    all_links = []
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)  # 回到页面顶部
    while len(all_links) < 300:  # 直到抓取到足够的链接为止
        prev_links_len = len(all_links)  # 记录上一次循环中的链接数量
        for _ in range(80):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)
            # 使用Selenium定位元素并抓取href属性
            elements = driver.find_elements(By.CSS_SELECTOR, "a[href]")
            links = [element.get_attribute('href') for element in elements]
            # 筛选贴文网址
            post_url_pattern = r'https://www.facebook.com/danny0425/posts/\w+'
            post_url_regex = re.compile(post_url_pattern)
            filtered_links = [link for link in links if post_url_regex.match(link)]
            # 检查并添加不重复的链接
            for link in filtered_links:
                if link not in all_links:
                    all_links.append(link)
                if len(all_links) >= 300:
                    break
            if len(all_links) >= 300:
                break
        # 如果上一次循环没有新增链接，则表示已经到达页面底部，退出循环
        if len(all_links) == prev_links_len:
            break
    final_links = list(set(all_links))
    return final_links[:300]  # 只返回前20个链接

def get_info_from_links(links: list[str]) -> list[dict]:
    result_data: list[dict] = []
    for link in links:
        service = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("headless")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(link)
        time.sleep(1)    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        target_span = soup.find('span', text="丹妮婊姐星球")
        try:
            time_info = soup.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm').find('span')
            content = soup.find('div', class_='x1iorvi4 x1pi30zi x1l90r2v x1swvt13') 
            like = soup.find('span', class_='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk')
            messages = soup.find('div', class_='x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1hl2dhg xggy1nq x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1ja2u2z xt0b8zv').find('span').text
            print("--------------------------------------------")
            print(target_span.text)
            print(f'日期:{time_info.text}')
            print(f'內文:{content.text}')
            print(f'讚數:{like.text}')
            print(f'留言數:{messages}')
            result_data.append({'title': target_span.text, 'date': time_info.text, 'content': content.text, 'likes': like.text, 'comments': messages})
        except:
            pass

    return result_data

def write_facebook_info_to_csv(facebook_data: list[dict], file_path: str):
    fieldnames = ['title', 'date', 'content', 'likes', 'comments']
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for idx, info in enumerate(facebook_data, start=1):
            writer.writerow(info)
            print(f"已成功寫入第 {idx} 筆資料到 CSV 文件中。")

    print("所有資料已成功寫入到 CSV 文件中。")

def main() -> None:
    email="----@gmail.com"
    password="----"
    chrome_url ='https://www.facebook.com/?locale=zh_TW'
    Danny_url = 'https://www.facebook.com/danny0425/?locale=zh_TW'
    url_list: list[str] = get_facebook_data(email, password, chrome_url, Danny_url)
    data: list[str] = get_info_from_links(url_list)
    write_facebook_info_to_csv(data, "fb_danny_post.csv")


if __name__ == "__main__":
    main()