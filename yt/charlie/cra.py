from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fun import get_video_urls, get_video_info , write_video_info_to_csv

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("headless")

channel_videos_url = "https://www.youtube.com/channel/UCyD3eaCai2yyWZEuczgZ-fw/videos"
csv_file_path = 'Charlie_video_info.csv'


if __name__ == '__main__':
    print("get video urls...")
    video_urls = get_video_urls(channel_videos_url)
    print("video_urls:", len(video_urls))
    print("get video info...")
    video_info = get_video_info(video_urls[:10], options)
    print("video_info:", len(video_info))
    print("write to csv...")
    write_video_info_to_csv(video_info, csv_file_path)