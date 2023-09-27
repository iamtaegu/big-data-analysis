import pdb
import time
import boto3
import datetime as dt
import json
import requests

from bs4 import BeautifulSoup

import warnings
# PythonDeprecationWarning을 무시하는 필터 추가
warnings.filterwarnings("ignore", category=DeprecationWarning)


def fetch_news_contents(msg):
#    print(msg)
    #print(msg.message_id)
    #print(msg.body)

    item = json.loads(msg.body)
    #print(item)

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

    resp = requests.get(item['url'], headers=headers)

    if resp.status_code != 200:
        return None

    soup = BeautifulSoup(resp.text, 'html.parser')

    node = soup.find("meta", {"property": "og:article:author"})
    if node:
        content = node['content']
        # print(content)

        if '네이버 스포츠' in content:
            return None
        if 'TV연애' in content:
            return None

        tokens = content.split('|')
        publisher = tokens[0].strip()

    else:
        pdb.set_trace()

    datestr_list, source_url = parse_media_info(soup)

    if len(datestr_list) == 1:
        created_at = parse_datestr(datestr_list[0])
        updated_at =- created_at

    elif len(datestr_list) == 2:
        created_at = parse_datestr(datestr_list[0])
        updated_at = parse_datestr(datestr_list[1])

    else:
        print(item)
        pdb.set_trace()

    print()
    print(publisher)
    print(created_at)
    print(updated_at)
    print(source_url)

    pdb.set_trace()
    pass

def parse_datestr(span):
    if span.has_attr('data-date-time'):
        datestr = span['data-date-time']
    elif span.has_attr('data-modify-date-time'):
        datestr = span['data-modify-date-time']
    else:
        return None

    date = dt.datetime.fromisoformat(datestr)

    return date

def parse_media_info(soup):
    media_info = soup.find("div", {"class": "media_end_head_info_datestamp"})
    print(media_info)

    if media_info:
        datestr_list = media_info.find_all("span", {"class":"media_end_head_info_datestamp_time"})

        link = media_info.find("a", {"class": "media_end_head_origin_link"})
        # 기사원문 버튼이 있는 경우와 없는 경우를 처리
        source_url = link['href'] if link else ''

        return datestr_list, source_url

    pdb.set_trace()


if __name__ == '__main__':
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='naver-news-list')

    while True:
        print(f'[{dt.datetime.now()}] Fetching news', end=' ', flush=True)

        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1,
        )

        #print(messages)

        if len(messages) == 0:
            print('- Queue is empty. Wait for a while..')
            time.sleep(60)
            continue

        #for msg in messages:
        #    msg.delete()

        buffer = []

        for msg in messages:
            print('.', end='', flush=True)

            entry = fetch_news_contents(msg)

            if entry:
                buffer.append(entry)

        print('!!')

        pdb.set_trace()
        pass

