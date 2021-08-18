from dotenv import load_dotenv

import os

from util import percent_to_zap_value
from zapper import Zapper, ZapTimer

load_dotenv()

API_NAME = os.getenv("PAVLOK_API_NAME", "test")
ZAP_LEVEL = percent_to_zap_value(int(os.getenv("PAVLOK_ZAP_PERCENT", 50)))
MESSAGE = os.getenv("PAVLOK_MESSAGE", "")

INTERVAL_MINUTES = float(os.getenv("PAVLOK_INTERVAL_MINUTES", 30))
INTERVAL_PERCENT = float(os.getenv("PAVLOK_INTERVAL_PERCENT", 20))

TIMEZONE = os.getenv("PAVLOK_TIMEZONE", "US/Pacific")
ASLEEP_BEFORE_HOUR = int(os.getenv("PAVLOK_ASLEEP_BEFORE_HOUR", 9))
ASLEEP_AFTER_HOUR = int(os.getenv("PAVLOK_ASLEEP_AFTER_HOUR", 21))

SLEEP_TIME_S = int(os.getenv("PAVLOK_SLEEP_TIME_S", 10))


def main():
    print("==== STARTING ZAPPER! ====")

    timer = ZapTimer(
        timezone_str=TIMEZONE,
        interval_minutes=INTERVAL_MINUTES,
        interval_percent=INTERVAL_PERCENT,
        sleep_hour_before=ASLEEP_BEFORE_HOUR,
        sleep_hour_after=ASLEEP_AFTER_HOUR,
    )

    Zapper(timer,
           api_name=API_NAME,
           zap_level=ZAP_LEVEL,
           message=MESSAGE,
           sleep_time_s=SLEEP_TIME_S
           ).run()

    print("==== ZAPPER STOPPED! ====")


if __name__ == "__main__":
    main()
