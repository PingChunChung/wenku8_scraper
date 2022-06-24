import requests as req
from bs4 import BeautifulSoup as bs
import os
import time
import random
from fake_useragent import UserAgent

ua = UserAgent(cache = True)

my_headers = {
    'user-agent':ua.random
    }



url = 'https://www.wenku8.net/modules/article/reader.php?aid=1'
res = req.get(url, headers = my_headers)
res.encoding = 'gbk'

soup = bs(res.text, 'lxml')


# 建立資料夾
file_path = soup.select_one('div#title').get_text()
if not os.path.exists(file_path):
    os.makedirs(file_path)
    
# 各集目錄
volumn_names = []
for i in soup.select('table.css tr td.vcss'):
    volumn_names.append(i.get_text())
    if not os.path.exists(f'{file_path}\{i.get_text()}'):
        os.makedirs(f'{file_path}\{i.get_text()}')


# 將各章連結存入list
url_chapt = []
titles = []
for i in soup.select('td.ccss> a'):
    url_chapt.append(i['href'])
    titles.append(i.get_text())
    
# 將小說內容抓下來存成txt
for index, link in enumerate(url_chapt):
    res = req.get(link, headers = my_headers)
    res.encoding = 'gbk'
    soup_link = bs(res.text, 'lxml')
    content = soup_link.select_one('div#content').get_text()
    for volumn_name in volumn_names:  #讓標題陣列去跟文章標題比對，如果一樣就文章標題的資料夾內
        if volumn_name in soup_link.select_one('title').get_text():
            with open(f'{file_path}\{volumn_name}\{titles[index]}.txt', 'w', encoding = 'utf-8') as f:
                f.write(content)
        time.sleep(random.random())
