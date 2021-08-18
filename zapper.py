from datetime import datetime, timedelta
import pytz
import requests
import time

from util import make_url, rand_minutes


class ZapTimer:
    def __init__(self, timezone_str, interval_minutes, interval_percent, sleep_hour_before, sleep_hour_after):
        self.timezone = pytz.timezone(timezone_str)
        self.interval_minutes = interval_minutes
        self.interval_percent = interval_percent

        self.sleep_hour_before = sleep_hour_before
        self.sleep_hour_after = sleep_hour_after

        self.next_time: datetime = self.get_next_time()

    def now(self) -> datetime:
        return datetime.now(self.timezone)

    def get_next_time(self) -> datetime:
        return self.now() + timedelta(minutes=rand_minutes(self.interval_minutes, self.interval_percent))

    def set_next_time(self):
        self.next_time = self.get_next_time()

    def sleep_time(self) -> bool:
        return self.next_time.hour < self.sleep_hour_before or self.next_time.hour > self.sleep_hour_after

    def time_remaining(self):
        return self.next_time - self.now()

    def time_to_zap(self) -> bool:
        if self.sleep_time():
            print(f"{self.now()} - It's sleeping time...")
            self.set_next_time()
            return False

        return self.time_remaining().total_seconds() <= 0


class Zapper:

    def __init__(self, timer: ZapTimer, api_name, zap_level, message="", sleep_time_s=5):
        self.timer = timer

        self.api_name = api_name
        self.zap_level = zap_level
        self.message = message

        self.sleep_time_s = sleep_time_s

    def now(self) -> datetime:
        return self.timer.now()

    def zap(self):
        try:
            url = make_url(self.api_name, self.zap_level, self.message)
            print(f"{self.now()} - Zapping to {url}")
            requests.get(url)
            self.timer.set_next_time()
        except Exception as e:
            print(f"{self.now()} - ERROR ZAPPING: {e}")

    def run(self):
        while True:
            time_left = self.timer.time_remaining()
            if self.timer.time_to_zap():
                print(f"{self.now()} - Not time yet ({time_left} remaining). Sleeping...")
            else:
                print(f"{self.now()} - It's time! ({time_left}). Zapping...")
                self.zap()
            time.sleep(self.sleep_time_s)
