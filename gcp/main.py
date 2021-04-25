import json
import os
from concurrent.futures.thread import ThreadPoolExecutor
from statistics import mean

import requests
from flask import Request
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.exceptions import TimeoutError
from google.cloud.pubsub_v1.subscriber.message import Message

TIMEOUT = 30
# TIMEOUT = 2 * 60
PROJECT_ID = "shikajiro-answers"
SUBSCRIPTION_ID = "mechatrax-test-sub"
TOPIC_ID = "mechatrax-test"

IMSI_LIST = [
    123456 # TODO IMSIを追記する。環境変数化してもいいかも
]


def start_batch(request: Request):
    request_json = request.get_json(silent=True)
    print(request_json)

    with ThreadPoolExecutor(max_workers=len(IMSI_LIST)) as executor:

        def call_up(imsi):
            data = {"body": "message"}
            headers = {
                "X-Soracom-API-Key": os.getenv("SORACOM_API_KEY"),
                "X-Soracom-Token": os.getenv("SORACOM_TOKEN")
            }
            res = requests.post(
                f"https://g.api.soracom.io/v1/subscribers/{imsi}/send_sms",
                json=data,
                headers=headers
            )
            print(json.loads(res.content))
            return res

        features = [executor.submit(call_up, imsi) for imsi in IMSI_LIST]
        for feature in features:
            print(f"result:{feature.result()}")

    sensors = []

    def callback(message: Message):
        print(f"Received {message}.")
        data = json.loads(message.data.decode("utf-8"))
        sensors.append(data)
        message.ack()

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            future.result(timeout=TIMEOUT)
        except TimeoutError:
            future.cancel()

    print(mean([sensor["temperature"] for sensor in sensors]))

    return json.dumps(sensors)


def receive_sensor(request: Request):
    request_json = request.get_json(silent=True)
    print(request.headers)
    print(request_json)

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    publisher.publish(topic_path, json.dumps(request_json).encode("utf-8"))
    return f'send temperature {request_json}!'
