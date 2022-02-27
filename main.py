import json
import requests
from os.path import basename
from os import mkdir
from bs4 import BeautifulSoup
from pytwitter import Api
import sys
from utils import parse_url
from yt_dlp import YoutubeDL
from selenium import webdriver
import time

with open('config.json', 'r') as f:
    config = json.load(f)

filename = sys.argv[1]

with open(filename, 'r') as f:
    list = f.readlines()

api = Api(config["BEARER_TOKEN"])
print(f'😎 TWEET SAVE 😎 SCRAPING INITIATED')
for line in list:
    url = line[0:-1]
    #url = "https://twitter.com/Tsihanouskaya/status/1497898169614708741"
    tweet_id = parse_url(url)

    #curl --request GET 'https://api.twitter.com/1.1/statuses/show.json?id=1497602699373645825&tweet_mode=extended' --header 'Authorization: Bearer AAAAAAAAAAAAAAAAAAAAACyvZgEAAAAAt0QaI6wQH9leUss6D1REBSn6FLc%3DaLMnJWehLL9YPuj7ZtKNXANT1ivLKCwxEDxbdYlL0h7rTLWGUD'
    try:
        response = api.get_tweet(tweet_id, expansions=['attachments.media_keys', 'author_id'], media_fields=['media_key'], user_fields=['id'])
    except:
        pass
    print(f'😎 TWEET SAVE 😎 SCRAPING TWEET: {tweet_id}')

    v_count = 0
    p_count = 0
    mkdir(f'tweet-{tweet_id}')
    try:
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
    except:
        pass


    with open(f'tweet-{tweet_id}/{tweet_id}.json', 'w') as f:
        json.dump({'tweet_id': tweet_id, "tweet_text": response.data.text, "author_id": response.includes.users[0].id, "author_name": response.includes.users[0].name, "author_handle": f'@{response.includes.users[0].username}'}, f, indent=4)

    print(f'😎 TWEET SAVE 😎 {tweet_id} SCRAPED')
#/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[2]/div/div/div/div/div/a/div/div[2]/div/img
#yld_opts = {'outtmpl': 'a/b.mp4'}
#with YoutubeDL(yld_opts) as ydl:
#    ydl.download(['https://twitter.com/Reevellp/status/1497663147771150347'])