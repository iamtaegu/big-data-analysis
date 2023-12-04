import pdb
import json
import requests
import pandas as pd
from config import *

def query_news_searchs(params):
    query = {
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

                fromDate = value[:4] + '-' + value[4:]
                toDate = ''

                day = int(value[4:])+1
                if day < 10:
                    toDate = value[:4] + '-' + '0' + str(day)
                else:
                    toDate = value[:4] + '-' + day

                query["query"]["bool"]["must"].append({
                    "range": {
                        "created_at": {
                            "gte": fromDate,
                            "lt": toDate
                        }
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
