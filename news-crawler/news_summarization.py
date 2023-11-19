import pdb
import json
import requests
import pandas as pd

from config import *
from transformers import pipeline
from googletrans import Translator

def fetch_missing_summary():
    body = {
        "query": {
            "bool": {
                # 특정 title
                "must": [
                    {
                        "match": {
                            "title": "삼성"
                        }
                    }
                ],
                "must_not": [
                    {
                        "exists": {
                            "field": "summary"
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

    assert resp.status_code == 200

    results = resp.json()

    hits = results['hits']['hits']
    docs = [x['_source'] for x in hits]

    df = pd.DataFrame(docs)
    df = df[['id', 'body']]

    return df

def upload_to_server(df):

    for _, row in df.iterrows():

        body = {
            "doc": {
                "summary": row.summary,
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

        assert resp.status_code == 200



if __name__ == '__main__':
    google = Translator()
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    while True:
        df = fetch_missing_summary()

        if df.empty:
            break

        body_list = df['body'].tolist()
        # 1. body > en_body
        en_body_output = google.translate(body_list, dest='en')
        en_body_list = [body_transleated.text for body_transleated in en_body_output]

        # 2. en_body > en_summary
        # default length 사용
        en_summary_output = summarizer(en_body_list)
        en_summary_list = [en_summary['summary_text'] for en_summary in en_summary_output]

        # 3. en_summary > ko_summary
        ko_body_output = google.translate(en_summary_list, dest='ko')
        ko_body_list = [ko_body.text for ko_body in ko_body_output]

        df['summary'] = ko_body_list

        upload_to_server(df)
