import requests
import random

SORACOM_FUNK_URL = "http://funk.soracom.io"


def main():
    data = {
        "device_id": "test_1",
        "temperature": random.randint(0, 40)
    }
    print(data)
    res = requests.post(SORACOM_FUNK_URL, json=data)
    print(res)
    print(res.content)


if __name__ == '__main__':
    main()
