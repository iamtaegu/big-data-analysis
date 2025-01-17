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

    # assert resp.status_code == 200

    if resp.status_code != 200:
        return ''

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

        # assert resp.status_code == 200

        if resp.status_code != 200:
            return ''


if __name__ == '__main__':
    google = Translator()
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    while True:
        df = fetch_missing_summary()

        if df.empty:
            break

        max_translate_length = 5000
        body_list = df['body'].tolist()
        body_list = [str for str in body_list if str] #빈 문자열 제거
        body_list = [str[:5000] for str in body_list]

        # 1. body > en_body

        # en_body_output = google.translate(body_list, dest='en')
        en_body_output = [google.translate(body, dest='en') for body in body_list]

        en_body_list = [body_transleated.text for body_transleated in en_body_output]

        # 2. en_body > en_summary
        # default length 사용
        max_sequence_length = 1024
        en_body_list_split = [en_body[:max_sequence_length] for en_body in en_body_list]
        en_summary_output = summarizer(en_body_list_split)
        en_summary_list = [en_summary['summary_text'] for en_summary in en_summary_output]

        # 3. en_summary > ko_summary
        #ko_body_output = google.translate(en_summary_list, dest='ko')
        ko_body_output = [google.translate(en_summary, dest='ko') for en_summary in en_summary_list]
        ko_body_list = [ko_body.text for ko_body in ko_body_output]

        # 빈 문자열 제거
        df['body'].replace('', pd.NA, inplace=True)
        df = df.dropna(subset=['body'])

        df['summary'] = ko_body_list

        print('------------------------------------upload_to_server------------------------------------')

        upload_to_server(df)
