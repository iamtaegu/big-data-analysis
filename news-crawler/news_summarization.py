import pdb
import json
import requests
import pandas as pd

from config import *
from transformers import pipeline

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

    assert resp.status_code == 200

    results = resp.json()

    hits = results['hits']['hits']
    docs = [x['_source'] for x in hits]

    df = pd.DataFrame(docs)
    df = df[['id', 'body']]

    return df

if __name__ == '__main__':
    summarizer = pipeline('summarization')

    text = "Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American entrepreneur, inventor, business magnate, media proprietor, and investor. He was the co-founder, chairman, and CEO of Apple; the chairman and majority shareholder of Pixar; a member of The Walt Disney Company's board of directors following its acquisition of Pixar; and the founder, chairman, and CEO of NeXT. He is widely recognized as a pioneer of the personal computer revolution of the 1970s and 1980s, along with his early business partner and fellow Apple co-founder Steve Wozniak."

    # 주어진 text를 64 길이 안으로 요약해줘
    df = pd.DataFrame(summarizer(text, max_length=64))

    print(df.summary_text.values[0])

    while True:
        df = fetch_missing_summary()

        if df.empty:
            break

        pdb.set_trace()

        bodies = df['body'].tolist()
        summaries = summarizer(bodies)

        df = df.join(summaries)

        pdb.set_trace()