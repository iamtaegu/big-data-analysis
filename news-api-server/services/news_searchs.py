
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
                    {
                        "exists": {
                            "field": "summary"
                        }
                    }
                ]
            }
        }
    }

    if params:
        for key, value in params.items():
            query["query"]["bool"]["must"].append({
                "match": {
                    key: value
                }
            })

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
