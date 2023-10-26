import os
import time
import json
from ylt import cache_dir

ratelimit_file = "ratelimit.json"
ratelimit_path = cache_dir + ratelimit_file


if not os.path.exists(ratelimit_path):
    with open(ratelimit_path, "w", encoding="utf-8") as file:
        file.write("{}")


def get_last_time(key):
    data = get_data()
    if key in data:
        return data[key]
    else:
        return -1


def overLimit(key, span_sec):
    sec = time.time() - get_last_time(key)
    return sec > span_sec, sec


def clear_old(data):
    for key in list(data.keys()):
        # 太久的，不保留
        if (time.time() - data[key] > 60 * 60 * 24 * 365):
            data.pop(key)
    return data


def saveRecord(key):
    data = get_data()
    data[key] = time.time()

    clear_old(data)

    json.dump(data, open(ratelimit_path, "w"), ensure_ascii=False, indent=4)


def get_data():
    return json.load(open(ratelimit_path, "r"))
