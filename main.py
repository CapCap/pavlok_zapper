import os

URL_BASE = "https://app.pavlok.com/unlocked/remotes/{}/zap/{}?message={}"


def make_url(name, level, message=""):
    return URL_BASE.format(name, level, message)
