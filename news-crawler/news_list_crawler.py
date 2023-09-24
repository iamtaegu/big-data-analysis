import pdb # Python debugger
import datetime as dt
import requests
import json
import boto3

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dateutil.relativedelta import relativedelta

def fetch_news_list(datestr, page):
    print (f'Fetching page {page}...')
    
    url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=101&date={datestr}&page={page}'

    headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' }

    resp = requests.get(url, headers=headers)

    # print (resp.status_code)
    # print (resp.text)

    soup = BeautifulSoup(resp.text, 'html.parser')

    list_body = soup.find("div", {"class":"list_body"})

    buffer = []

    for item in list_body.find_all("li"):
        link = item.find_all("a")[-1]
        title = link.text.strip()

        href = link['href']
        parsed_url = urlparse(href)

        tokens = parsed_url.path.split('/')
        msg_id = 'nn-' + '-'.join(tokens[-2:])

        # print(title)
        # print(href)
        # print(parsed_url)
        # print(tokens)
        # print(msg_id)

        body = {
            'msg_id' : msg_id,
            'title' : title,
            'url' : href,
        }

        entry = {
            'Id': msg_id,
            'MessageBody': json.dumps(body) # dict to json 
        }

        buffer.append(entry)

    return buffer

''' 
    마지막 페이지 체크 포인트 2개
        ㅁ last_id 비교 - 네이버에서 마지막 페이지는 처음 페이지 id를 줌
        ㅁ 버퍼 크기 20 이하 체크 
'''
def fetch_news_list_for_date(date):
    datestr = date.strftime('%Y%m%d')
    
    print('[{}] Fetching news list on {} ...'.format(dt.datetime.now(), datestr))

    last_id = None
    
    for page in range(1, 1000):
        buffer = fetch_news_list(datestr, page)

        if last_id == buffer[-1]['Id']:
            break
        else:
            last_id = buffer[-1]['Id']

        push_to_aws_queue(buffer)

        if len(buffer) < 20:
            break

def push_to_aws_queue(buffer):
    print('Pushing to AWS SQS')

    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName = 'naver-news-list')

    # remove duplicate msg id 
    # 아래는 dict 형태이기 때문에 중복된 key는 overriding 됨 
    temp = { x['Id']: x for x in buffer }
    buffer = list(temp.values())

    for idx in range(0, len(buffer), 10): 
        chunk = buffer[idx:idx+10]
        queue.send_messages(Entries=chunk)


if __name__ == '__main__':
    base_date = dt.datetime(2023, 8, 1)

    for d in range(45):
        date = base_date + relativedelta(days=d)

        fetch_news_list_for_date(date);
