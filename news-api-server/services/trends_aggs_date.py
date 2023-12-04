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
                    toDate = value[:4] + '-' + '01'
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

    print(query)

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

    return results

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
