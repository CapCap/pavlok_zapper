from random import uniform
from urllib.parse import quote_plus

URL_BASE = "https://app.pavlok.com/unlocked/remotes/{}/zap/{}?message={}"


def make_url(api_name, level, message=""):
    return URL_BASE.format(api_name, level, quote_plus(message))


def rand_minutes(interval_minutes, interval_percent):
    start_interval = interval_minutes * (1 - interval_percent / 100)
    return uniform(start_interval, interval_minutes)


def percent_to_zap_value(zap_percent):
    return int(zap_percent * 255 / 100)
