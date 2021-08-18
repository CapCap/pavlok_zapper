from datetime import datetime
from dateutil import tz
import unittest
from freezegun import freeze_time

from zapper import Zapper, ZapTimer
from util import make_url, rand_minutes, percent_to_zap_value


class TestUtils(unittest.TestCase):

    def test_make_url(self):
        url = make_url(api_name="test_name", level=101, message="testing spaces")
        self.assertEqual(url, "https://app.pavlok.com/unlocked/remotes/test_name/zap/101?message=testing+spaces")

    def test_rand_minutes(self):
        for _ in range(1000):
            minutes = rand_minutes(100, 10)
            self.assertTrue(90 <= minutes <= 100)

    def test_percent_to_zap_value(self):
        self.assertEqual(percent_to_zap_value(45), 114)
        self.assertEqual(percent_to_zap_value(60), 153)


def make_timer() -> ZapTimer:
    return ZapTimer(
        timezone_str="US/Pacific",
        interval_minutes=30,
        interval_percent=10,
        sleep_hour_before=8,
        sleep_hour_after=18,
    )


TZ = tz.gettz("America/Los Angeles")


def parse_time(time) -> datetime:
    # work around weird bug in `freeze_time`
    dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return dt.astimezone(TZ)


class TestZapTimer(unittest.TestCase):

    def test_sleep_times(self):
        for time in ["2021-01-01 7:10:00", "2021-01-01 19:10:00"]:
            with freeze_time(parse_time(time)):
                timer = make_timer()
                timer.next_time = timer.now()
                self.assertTrue(timer.sleep_time(), msg=f"should have slept at {time}")

    def test_zap_times(self):
        for time in ["2021-01-01 8:10:00", "2021-01-01 12:10:00", "2021-01-01 17:59:00"]:
            with freeze_time(parse_time(time)):
                timer = make_timer()
                timer.next_time = timer.now()
                self.assertTrue(timer.time_to_zap(), msg=f"should have zapped at {time}")

    def test_get_next_time(self):
        with freeze_time(parse_time("2021-01-01 12:00:00")):
            for _ in range(1000):
                timer = make_timer()
                d = timer.get_next_time() - timer.now()
                self.assertTrue(27 <= (d.seconds / 60) < 30)


if __name__ == '__main__':
    unittest.main()
