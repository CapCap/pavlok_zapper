from datetime import datetime, timedelta
import os
import pytz
from random import uniform
import requests
import time

URL_BASE = "https://app.pavlok.com/unlocked/remotes/{}/zap/{}?message={}"

PAVLOK_API_NAME = os.getenv("PAVLOK_API_NAME", "test")

ZAP_LEVEL = 100

INTERVAL_MINUTES = 30

INTERVAL_PERCENT = 10


def make_url(level, message=""):
    return URL_BASE.format(PAVLOK_API_NAME, level, message)


def rand_minutes():
    percent_unit = INTERVAL_MINUTES * (INTERVAL_PERCENT / 100)
    return uniform(INTERVAL_MINUTES - percent_unit, INTERVAL_MINUTES + percent_unit)


def now_pst():
    return datetime.now(pytz.timezone('US/Pacific'))


class Zapper:

    def __init__(self):
        self._next_time = None
        self.set_next_time()

    def set_next_time(self):
        self._next_time = now_pst() + timedelta(minutes=rand_minutes())

    def zap(self):
        if self._next_time.hour < 10 or self._next_time.hour > 20:
            print(f"{now_pst()} - JK! is sleeping time...")
            self.set_next_time()
            return

        try:
            url = make_url(ZAP_LEVEL)
            print(f"{now_pst()} - Zapping to {url}")
            requests.get(url)
            self.set_next_time()
        except Exception as e:
            print(f"{now_pst()} - ERROR ZAPPING: {e}")

    def time_remaining(self):
        return self._next_time - now_pst()

    def run(self):
        while True:
            if self.time_remaining().total_seconds() > 0:
                print(f"{now_pst()} - Not time yet ({self.time_remaining()} remaining). Sleeping...")
            else:
                print(f"{now_pst()} - It's time! ({self.time_remaining()}). Zapping...")
                self.zap()
            time.sleep(5)


def main():
    Zapper().run()


if __name__ == "__main__":
    main()
