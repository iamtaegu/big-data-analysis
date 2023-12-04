import pdb
import json
import requests
import pandas as pd
from config import *

def query_news_searchs(params):
    query = {
        "size": 0,
        "aggs": {
            "group_by_date": {
                "date_histogram": {
                    "field": "created_at",
                    "interval": "day"
                }
            }
        },
        "query": {
            "bool": {
                "must": [
                ]
            }
        }
    }

    targetQuery = ''

    # SELECT * FROM TABLE WHERE key like '%value%'
    # AND (created_at >= value AND created_at < date)
    if params:
        for key, value in params.items():
            if "date" == key:

                if len(value) == 0:
                    continue

                fromDate = value[:4] + '-' + value[4:]
                toDate = ''

                day = int(value[4:])+1

                if day == 13:
                    toDate = str(int(value[:4]) + 1) + '-' + '01'
                elif day < 10:
                    toDate = value[:4] + '-' + '0' + str(day)
                else:
                    toDate = value[:4] + '-' + str(day)

                query["query"]["bool"]["must"].append({
                    "range": {
                        "created_at": {
                            "gte": fromDate,
                            "lt": toDate
                        }
                    }
                })
            elif "sentiment" == key:

                targetQuery = "sentiment"

                query['aggs']['group_by_date']['aggs'] = {
                    "group_by_sentiment": {
                        "terms": {
                            "field": "sentiment.keyword"
                        }
                    }
                }

            elif "title" == key:

                if len(value) > 0:
                    query["query"]["bool"]["must"].append({
                        "match": {
                            key: value
                        }
                    })

            else :
                query["query"]["bool"]["must"].append({
                    "match": {
                        key: value
                    }
                })

    query = json.dumps(query)

    print(query)

    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.get(
        f"{ELASTICSEARCH_URL}/news/_search",
        headers=headers,
        data = query,
        auth = ELASTICSEARCH_AUTH,
    )

    # 클라이언트에서 사용하기 편하게
    # 응답값 변환
    results = resp.json()
    buckets = results['aggregations']['group_by_date']['buckets']
    df = pd.DataFrame()
    if "sentiment" == targetQuery:
        buffer = []

        # 중첩된 데이터를 한 줄로 변경
        for x in buckets:
            sents = x['group_by_sentiment']['buckets']

            entry = {t['key']: t['doc_count'] for t in sents}
            entry['date'] = x['key_as_string']

            buffer.append(entry)

        if len(buffer) == 0:
            return []

        df = convert_sentiment_trends(buffer)
    elif "title" == targetQuery:
        df = convert_news_trends(buckets)
    else:
        df

    return df.to_dict(orient='records')

def convert_news_trends(buckets):
    df = pd.DataFrame(buckets)
    df['date'] = df['key_as_string'].str[:10]
    df = df[['date', 'doc_count']]

    return df

def convert_sentiment_trends(buffer):

    df = pd.DataFrame(buffer)
    df['date'] = df['date'].str[:10]

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
    df = df.reset_index()

    return df

def main(event, context):
    params = event.get('queryStringParameters')

    bodys = query_news_searchs(params)

    body = {
        'message': bodys
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
