import requests
from multiprocessing import Pool
from requests.exceptions  import RequestException
import re
import json

#获取页面信息
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#解析页面
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?<a.*?>.*?<img.*?src=".*?".*?>.*?<img.*?src="(.*?)".*?>.*?</a>.*?name"><a.*?>(.*?)</a>.*?</p>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?score".*?integer".*?>(.*?)</i>.*?fraction">(.*?)</i>.*?</p>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip(),
            'date':item[4].strip(),
            'score':item[5]+item[6]
        }

#写入文件
def write_to_file(content):
    with open('top.txt','a', encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

#主方法
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    for item in parse_one_page(get_one_page(url)):
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main,{i*10 for i in range(10)})
