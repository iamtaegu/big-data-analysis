import pdb
import time
import boto3
import datetime as dt
import json
import requests

from bs4 import BeautifulSoup

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
        print(content)

        if '네이버 스포츠' in content:
            return None
        if 'TV연애' in content:
            return None

        tokens = content.split('|')
        publisher = tokens[0].strip()

    else:
        pdb.set_trace()

    print()
    print(publisher)

    pdb.set_trace()
    pass

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

