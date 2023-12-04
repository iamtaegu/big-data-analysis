import pdb
import json
import requests
import pandas as pd
from config import *

def query_sentiment_trends(search):
    query = {
        "size": 0,
        "aggs": {
            "group_by_date": {
                "date_histogram": {
                    "field": "created_at",
                    "interval": "day"
                },
                "aggs": {
                    "group_by_sentiment": {
                        "terms": {
                            "field": "sentiment.keyword"
                        }
                    }
                }
            }
        }
    }
    
    if search:
        query['query'] = {
            'match': {
                'title': search
            }
        }

    print (query)


    query = json.dumps(query)

    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.get(
        f"{ELASTICSEARCH_URL}/news/_search",
        headers=headers,
        data = query,
        auth = ELASTICSEARCH_AUTH,
    )

    results = resp.json()

    buckets = results['aggregations']['group_by_date']['buckets']

    buffer = []

    # 중첩된 데이터를 한 줄로 변경
    for x in buckets:
        #print(json.dumps(x, indent=4))

        sents = x['group_by_sentiment']['buckets']

        # entry = {}
        # for s in sents:
        #     key = x['key']
        #     value = x['doc_count']
        #     entry[key] = value

        entry = {t['key']: t['doc_count'] for t in sents}
        entry['date'] = x['key_as_string']

        buffer.append(entry)

    if len(buffer)  == 0:
        return [] 

    df = pd.DataFrame(buffer)
    df['date'] = df['date'].str[:10]

    # date에서 문자열 더하기가 안되는데, set_index를 통해 더하기 대상에서 제외시킴 
    # pdb.set_trace() 

    df = df.set_index('date')
    df = df.fillna(0)       

    # 컬럼이 존재하지 않을 경우를 처리 
    if 'positive' not in df.columns:
        df['positive'] = 0
    if 'negative' not in df.columns:
        df['negative'] = 0

    df['sentiment'] = \
        (df['positive'] - df['negative']) / df.sum(axis=1)

    df = df.dropna()
    # 위에서 set_index 설정한 것을 원복시킴
    df = df.reset_index()

    return df.to_dict(orient='records')

def main(event, context):
    params = event.get('queryStringParameters')

    if params:
        search = params.get('search')
    else:
        search = None

    trends = query_sentiment_trends(search)

    body = {
        'message': trends        
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        # CORS
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        }
    }

    return response