import json
import requests
from config import *
from transformers import pipeline

def req_text_generation(params):

    if params:

        # gpt2 다운 받음
        generator = pipeline('text-generation', model="gpt2")

        text = params.get('contents')

        return generator(text, max_length=128)

def main(event, context):
    params = event.get('queryStringParameters')

    bodys = req_text_generation(params)

    body = {
        'message': bodys
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        }
    }

    return response