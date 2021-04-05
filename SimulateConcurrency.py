import requests
import logging
import threading
import time
import random
logging.getLogger().setLevel(logging.INFO)


def main():
    api = ["http://localhost:5004/buy/2",
           "http://localhost:5002/catalog/update"]

    data = {"id": 2, "stock": 2000, "cost": 2000}

    call = random.choice(api)
    logging.info("Calling request %s ", call)
    if (call == api[1]):
        response = requests.put(
            "http://localhost:5002/catalog/update", json=data)
    else:
        response = requests.post("http://localhost:5004/buy/2")

    logging.info("Response: %s ", response.text)


if __name__ == "__main__":
    threads = list()
    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=main)
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
