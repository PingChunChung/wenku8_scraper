import requests as req
from bs4 import BeautifulSoup as bs
import time
import random
from fake_useragent import UserAgent

ua = UserAgent(cache = True)

my_headers = {
    'user-agent':ua.random
    }

titles = []
num = 1


Flag = True
break_time = 0
while Flag:   
    try:
        
        url = f'https://www.wenku8.net/book/{num}.htm'
        res = req.get(url, headers = my_headers)
        res.encoding = 'gbk'
    
        soup = bs(res.text, 'lxml')
        
        check = soup.select_one('title').get_text()
        if check == '出现错误':
            num += 1
            break_time += 1
            time.sleep(random.randint(1,3))
            continue
        
        else:
            titles.append(f"{num} : {soup.select_one('span > b').get_text()}")
            num += 1
            break_time = 0
            time.sleep(random.randint(1,3))
        
        if time == 10:
            break
        
    except Exception:
        Flag = False
    
with open('novel_list.txt', 'w', encoding='utf-8') as f:
    for title in titles:
        f.write(title + '\n')