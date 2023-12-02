import pdb
import json
import requests
import pandas as pd

from config import * 
from transformers import pipeline

# sentiments가 없는 news를 가져옴 
def fetch_missing_sentiments():
    body = {
        "query": {
            "bool": {
                "must_not": [
                    {
                        "exists": {
                            "field": "sentiment"
                        }
                    }
                ]
            }
        }
    }

    body = json.dumps(body)

    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.get(
        f'{ELASTICSEARCH_URL}/news/_search',
        headers=headers,
        data=body,
        auth=ELASTICSEARCH_AUTH,
    )

    if resp.status_code != 200:
        return ''

    # print(resp)

    results = resp.json()

    hits = results['hits']['hits']
    docs = [x['_source'] for x in hits]

    df = pd.DataFrame(docs)
    df = df[['id', 'title']]

    return df

def upload_to_server(df):

    for _, row in df.iterrows():

        body = {
            "doc": {
                "sentiment": row.label,                
            }

        }
        body = json.dumps(body)

        headers = {
            'Content-Type': 'application/json'
        }

        # _update로 주지 않으면 override 됨 
        resp = requests.post(
                f"{ELASTICSEARCH_URL}/news/_update/{row['id']}",
                headers=headers,
                data=body,
                auth=ELASTICSEARCH_AUTH,
        )

        print('------------------------------------upload_to_server------------------------------------')

        if resp.status_code != 200:
            return ''


if __name__ == '__main__':

    classifier = pipeline('sentiment-analysis', model='snunlp/KR-FinBert-SC')

    while True: 
        df = fetch_missing_sentiments()

        if df.empty:
            break
        
        titles = df['title'].tolist()
        sentiments = classifier(titles)

        df_sents = pd.DataFrame(sentiments)
        df_sents = df_sents[['label']]

        df = df.join(df_sents)
        print(df)

        upload_to_server(df)