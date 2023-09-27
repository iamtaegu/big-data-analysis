import pdb
import time
import boto3
import datetime as dt

def fetch_news_contents(msg):
#    print(msg)
    print(msg.message_id)
    print(msg.body)

    pdb.set_trace()
    pass

if __name__ == '__main__':
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='naver-news-list')

    while True:
        print(f'[{dt.datetime.now()}] Fetching news', end=' ', flush=True)

        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1,
        )

        #print(messages)

        if len(messages) == 0:
            print('- Queue is empty. Wait for a while..')
            time.sleep(60)
            continue

        #for msg in messages:
        #    msg.delete()

        buffer = []

        for msg in messages:
            print('.', end='', flush=True)

            entry = fetch_news_contents(msg)

            if entry:
                buffer.append(entry)

        print('!!')

        pdb.set_trace()
        pass

