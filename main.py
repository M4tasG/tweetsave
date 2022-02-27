import json
from nturl2path import url2pathname
import requests
from os.path import basename
from os import mkdir
from bs4 import BeautifulSoup
from pytwitter import Api
from utils import parse_url
from yt_dlp import YoutubeDL
from selenium import webdriver
import time

with open('config.json', 'r') as f:
    config = json.load(f)

api = Api(config["BEARER_TOKEN"])
url = "https://twitter.com/Benson75844464/status/1497631611181047816"
tweet_id = parse_url(url)

#curl --request GET 'https://api.twitter.com/1.1/statuses/show.json?id=1497602699373645825&tweet_mode=extended' --header 'Authorization: Bearer AAAAAAAAAAAAAAAAAAAAACyvZgEAAAAAt0QaI6wQH9leUss6D1REBSn6FLc%3DaLMnJWehLL9YPuj7ZtKNXANT1ivLKCwxEDxbdYlL0h7rTLWGUD'

response = api.get_tweet(tweet_id, expansions=['attachments.media_keys'], media_fields=['media_key'])

print(response)

v_count = 0
p_count = 0
mkdir(f'tweet-{tweet_id}')
for ent in response.includes.media:
    if(ent.type == 'video'):
        v_count += 1
        yld_opts = {'outtmpl': f'tweet-{tweet_id}/{tweet_id}-video-{v_count}.mp4'}
        with YoutubeDL(yld_opts) as ydl:
            ydl.download([url])
    elif(ent.type == 'photo'):
        p_count += 1
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(1.5)
        html = driver.page_source
        page = BeautifulSoup(html, 'html.parser')
        #page = BeautifulSoup(requests.get(url).content, 'html.parser')
        img = page.find_all('img', class_='css-9pa8cd')
        img_src = img[p_count].get('src')
        img = requests.get(img_src)
        with open(f'tweet-{tweet_id}/{tweet_id}-image-{p_count}.png', 'wb') as f:
            f.write(img.content)
        driver.close()
    else:
        pass



#/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[2]/div/div/div/div/div/a/div/div[2]/div/img
#yld_opts = {'outtmpl': 'a/b.mp4'}
#with YoutubeDL(yld_opts) as ydl:
#    ydl.download(['https://twitter.com/Reevellp/status/1497663147771150347'])